import omni.kit.app
import omni.usd
from petrl.tools.lightblending.distant_light_model import DistantLightModel
from pxr import Usd, UsdLux, UsdGeom, Gf, Tf
from .distant_light_model import DistantLightModel
from .sphere_light_model import SphereLightModel
from .utils import LightUtils

__all__ = ["LightingSystem"]


class LightingSystem():
    instance = None

    def startup(self, viewport_scene):
        self._tracked_lights = []
        self._light_models = []

        self._viewport_scene = viewport_scene

        app = omni.kit.app.get_app()

        # Subscribe to update loop
        self._update_end_sub = app.get_update_event_stream().create_subscription_to_pop(
            self._on_update,
            name="LightingSystem"
        )

        # Listen for object selection changes
        self._events = self._usd_context.get_stage_event_stream()
        self._stage_event_sub = self._events.create_subscription_to_pop(
            self._on_stage_event, name="Light Manipulator Selection Change"
        )

        # Listen for changes in objects
        stage = self._usd_context.get_stage()
        self._stage_listener = Tf.Notice.Register(Usd.Notice.ObjectsChanged, self._notice_changed, stage)

    def shutdown(self):
        for model in self._light_models:
            print("Cleaning up light model: ", model)
            model.on_shutdown()

        if hasattr(self, "_update_end_sub") and self._update_end_sub is not None:
            print("Unsubscribe from update event stream")
            self._update_end_sub.unsubscribe()

        if hasattr(self, "_stage_event_sub") and self._stage_event_sub is not None:
            print("Unsubscribe from stage event stream")
            self._stage_event_sub.unsubscribe()

        if hasattr(self, "_stage_listener") and self._stage_listener:
            print("Unregistered stage listener")
            self._stage_listener.Revoke()
            self._stage_listener = None

        self._tracked_lights = []
        self._light_models = []

    def add_light(self, light):
        if not light.IsA(UsdLux.Light):
            print('Selected primitive is not light: ', light)
            return

        if light not in self._tracked_lights:
            model = None
            if light.IsA(UsdLux.DistantLight):
                model = DistantLightModel(light)
            elif light.IsA(UsdLux.SphereLight):
                model = SphereLightModel(light)

            if not model:
                print("Light is not supported: ", light)
                return

            print("Tracking new light: ", light)

            self._tracked_lights.append(light)
            self._light_models.append(model)

            self._on_kit_selection_changed()
        else:
            print("Light is already being tracked!")

    def remove_light(self, light_to_remove):
        for light, model in zip(self._tracked_lights, self._light_models):
            if light == light_to_remove:
                print("Stopped tracking light: ", light)
                model.on_shutdown()
                self._tracked_lights.remove(light_to_remove)
                self._light_models.remove(model)
                break

    def get_all_lights_of_type(self, light_type: UsdLux.Light):
        result = []

        for light, model in zip(self._tracked_lights, self._light_models):
            if light.IsA(light_type):
                result.append((light, model))

        return result

    def has_light(self, light):
        return light in self._tracked_lights

    def _on_update(self, args):
        camera_position = Gf.Vec3f(LightUtils.get_camera_position())
        # print("Active camera position: ", camera_position)

        try:
            self.update_sphere_lights(camera_position)
            # self.update_dsstant_lights(camera_position)

        except Exception as exc:
            print("Exception when updating lights: ", exc)

    def update_sphere_lights(self, camera_position):
        for light, model in self.get_all_lights_of_type(UsdLux.SphereLight):
            light_position = LightUtils.get_light_position(light)

            distance_to_camera = (camera_position - light_position).GetLength()

            light_weight = float(distance_to_camera / (model.get_radius() + 0.0001))
            # print("Light weight: ", light_weight)

            new_intensity = 1.0 - min(1.0, light_weight)
            # print(new_intensity)
            new_intensity = new_intensity * model.get_default_intensity()
            # print(new_intensity)
            # print("New intensity: ", new_intensity)

            model.set_intensity(new_intensity)

    def update_distant_lights(self, camera_position):
        for light, model in self.get_all_lights_of_type(UsdLux.DistantLight):
            # todo: think how to support distant lights
            pass

    @staticmethod
    def get_instance():
        if LightingSystem.instance is None:
            # print("creating new lighting system")
            LightingSystem.instance = LightingSystem()

        return LightingSystem.instance

    def _on_stage_event(self, event):
        """Called by stage_event_stream"""
        if event.type == int(omni.usd.StageEventType.SELECTION_CHANGED):
            self._on_kit_selection_changed()

    @property
    def _usd_context(self) -> Usd.Stage:
        # Get the UsdContext we are attached to
        return omni.usd.get_context()

    def _on_kit_selection_changed(self):
        usd_context = self._usd_context
        if not usd_context:
            self._viewport_scene.set_model(None)
            return

        stage = usd_context.get_stage()
        if not stage:
            self._viewport_scene.set_model(None)
            return

        prim_paths = usd_context.get_selection().get_selected_prim_paths() if usd_context else None
        if not prim_paths:
            self._viewport_scene.set_model(None)
            return

        selected_prim_path = prim_paths[0]

        for _, model in self.get_all_lights_of_type(UsdLux.DistantLight):
            if model.get_light_path() == selected_prim_path:
                self._viewport_scene.set_model(model)
                return

        self._viewport_scene.set_model(None)

    def _notice_changed(self, notice, stage):
        """Called by Tf.Notice. When USD data changes, we update light model"""

        changed_items = set()

        for p in notice.GetChangedInfoOnlyPaths():
            prim_path = p.GetPrimPath().pathString

            for _, model in self.get_all_lights_of_type(UsdLux.DistantLight):
                if model.get_light_path() != prim_path:
                    continue

                print("Attribute changed: ", p.name)

                if p.name == "intensity":
                    prim = stage.GetPrimAtPath(prim_path)
                    usd_light = UsdLux.Light(prim)

                    print("Light intensity changed for object: ", usd_light)

                    # self._intensity = usd_light.GetIntensityAttr().Get()
                    # changed_items.add(self._intensity)

                    # print("Light intensity changed to: ", self._intensity)
                elif p.name == "radius":
                    model.mark_as_dirty()
                elif "translate" in p.name:
                    model.mark_as_dirty()

            # todo: any plans to use it?
            for item in changed_items:
                self._item_changed(item)
