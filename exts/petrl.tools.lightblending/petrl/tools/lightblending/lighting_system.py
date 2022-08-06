import omni.kit.app
import omni.usd
from pxr import UsdLux, UsdGeom, Gf
from .light_model import LightModel
from .utils import LightUtils

__all__ = ["LightingSystem"]


class LightingSystem():
    instance = None

    def startup(self, viewport_scene):
        self._tracked_lights = []
        self._light_models = []

        self._viewport_scene = viewport_scene

        app = omni.kit.app.get_app()

        self._update_end_sub = app.get_update_event_stream().create_subscription_to_pop(
            self._on_update,
            name="LightingSystem"
        )

    def shutdown(self):
        for model in self._light_models:
            print("Cleaning up light model: ", model)
            model.cleanup_listeners()

        if hasattr(self, "_update_end_sub") and self._update_end_sub is not None:
            print("Unsubscribe from update event stream")
            self._update_end_sub.unsubscribe()

        self._tracked_lights = []
        self._light_models = []

    def add_light(self, light):
        if not light.IsA(UsdLux.Light):
            print('Selected primitive is not light: ', light)
            return

        if light not in self._tracked_lights:
            print("Tracking new light: ", light)
            self._tracked_lights.append(light)

            model = LightModel(light)
            self._light_models.append(model)

            if light.IsA(UsdLux.DistantLight):
                self._viewport_scene.set_light_model(model)
        else:
            print("Light is already being tracked!")

    def get_all_lights_of_type(self, light_type: UsdLux.Light):
        result = []

        for light, model in zip(self._tracked_lights, self._light_models):
            if light.IsA(light_type):
                result.append((light, model))

        return result

    def remove_light(self, light):
        # todo: remove light and its model
        pass

    def has_light(self, light):
        return light in self._tracked_lights

    def _on_update(self, args):
        # todo: enable
        # camera_position = Gf.Vec3f(LightUtils.GetCameraPosition())
        # print("Active camera position: ", camera_position)

        try:
            z = 2
            # self.update_sphere_lights(camera_position)
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
