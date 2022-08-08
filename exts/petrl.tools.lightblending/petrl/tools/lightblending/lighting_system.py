import omni.kit.app
import omni.usd
from pxr import Usd, Gf, Tf
from .models import LightModelFactory
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
        events = self._usd_context.get_stage_event_stream()
        self._stage_event_sub = events.create_subscription_to_pop(
            self._on_stage_event, name="Light Manipulator Selection Change"
        )

        # Listen for changes in objects
        stage = self._usd_context.get_stage()
        self._stage_listener = Tf.Notice.Register(Usd.Notice.ObjectsChanged, self._notice_changed, stage)

    def shutdown(self):
        for model in self._light_models:
            print("Cleaning up light model: ", model)
            if model:
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
        self._viewport_scene = None

    def on_stage_changed(self):
        self._tracked_lights = []
        self._light_models = []

    def add_light(self, light):
        if light not in self._tracked_lights:
            model = LightModelFactory.new_model(light)
            if not model:
                print("Light is not supported: ", light)
                return

            print("Tracking new light: ", light)

            self._tracked_lights.append(light)
            self._light_models.append(model)

            self._update_viewport_scene(model)
        else:
            print("Light is already being tracked!")

    def remove_light(self, light):
        if light in self._tracked_lights:
            print("Stopped tracking light: ", light)
            index = self._tracked_lights.index(light)
            del self._tracked_lights[index]
            model = self._light_models.pop(index)
            model.on_shutdown()

            self._update_viewport_scene(None)

    def has_light(self, light):
        return light in self._tracked_lights

    def _on_update(self, args):
        if len(self._light_models) > 0:
            camera_position = Gf.Vec3f(LightUtils.get_camera_position())
            if not camera_position:
                return

        try:
            for model in self._light_models:
                model.update_light_intensity(camera_position)

        except Exception as exc:
            print("Exception when updating lights: ", exc)

    @staticmethod
    def get_instance():
        if LightingSystem.instance is None:
            LightingSystem.instance = LightingSystem()

        return LightingSystem.instance

    def _on_stage_event(self, event):
        """Called by stage_event_stream"""
        if event.type == int(omni.usd.StageEventType.SELECTION_CHANGED):
            model = self._on_kit_selection_changed()
            self._update_viewport_scene(model)

    def _update_viewport_scene(self, model):
        if self._viewport_scene:
            if model and model.has_visualizer():
                self._viewport_scene.set_model(model)
            else:
                self._viewport_scene.set_model(None)

    @property
    def _usd_context(self) -> Usd.Stage:
        # Get the UsdContext we are attached to
        return omni.usd.get_context()

    def _on_kit_selection_changed(self):
        if not self._viewport_scene:
            return None

        usd_context = self._usd_context
        if not usd_context:
            return None

        stage = usd_context.get_stage()
        if not stage:
            return None

        prim_paths = usd_context.get_selection().get_selected_prim_paths() if usd_context else None
        if not prim_paths:
            return None

        selected_prim_path = prim_paths[0]

        for model in self._light_models:
            if model and model.get_light_path() == selected_prim_path:
                return model

        return None

    def _notice_changed(self, notice, stage):
        """Called by Tf.Notice. When USD data changes, we update light model"""

        if not stage:
            return

        for p in notice.GetChangedInfoOnlyPaths():
            prim_path = p.GetPrimPath().pathString

            for model in self._light_models:
                if model and model.get_light_path() == prim_path:
                    model.on_changed(p.name)
