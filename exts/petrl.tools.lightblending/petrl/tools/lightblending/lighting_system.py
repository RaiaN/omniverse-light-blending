import omni.kit.app
from pxr import UsdLux, UsdGeom, Gf
from pxr.Usd import TimeCode

from .light_model import LightModel
from .camera_utils import CameraUtils

__all__ = ["LightingSystem"]


class LightingSystem():
    instance = None

    def startup(self):
        app = omni.kit.app.get_app()

        self._update_end_sub = app.get_update_event_stream().create_subscription_to_pop(
            self._on_update,
            name="LightingSystem"
        )

        self.tracked_lights = []
        self.light_models = []

    def shutdown(self):
        for model in self.light_models:
            print("Cleaning up light model: ", model)
            model.cleanup_listeners()

        if hasattr(self, "_update_end_sub") and self._update_end_sub is not None:
            print("Unsubscribe from update event stream")
            self._update_end_sub.unsubscribe()

        self.tracked_lights = []
        self.light_models = []

    def add_light(self, light):
        if not light.IsA(UsdLux.Light):
            print('Selected primitive is not light: ', light)
            return

        if light not in self.tracked_lights:
            print("Tracking new light: ", light)
            self.tracked_lights.append(light)
            self.light_models.append(LightModel(light))
        else:
            print("Light is already being tracked!")

    def get_all_lights_of_type(self, light_type: UsdLux.Light):
        result = []

        for light, model in zip(self.tracked_lights, self.light_models):
            if light.IsA(light_type):
                result.append((light, model))

        return result

    def remove_light(self, light):
        # todo
        # print(light)
        pass

    def has_light(self, light):
        return light in self.tracked_lights

    @staticmethod
    def get_sphere_light_position(light):
        light_prim = UsdGeom.Imageable(light)
        _, _, _, position = light_prim.ComputeLocalToWorldTransform(TimeCode())
        position = position[:3]
        position = Gf.Vec3f(position)

        return position

    def _on_update(self, args):
        camera_position = Gf.Vec3f(CameraUtils.GetCameraPosition())
        # print("Active camera position: ", camera_position)

        try:
            self.update_sphere_lights(camera_position)
            self.update_distant_lights(camera_position)

        except Exception as exc:
            print("Exception when updating lights: ", exc)

    def update_sphere_lights(self, camera_position):
        for light, model in self.get_all_lights_of_type(UsdLux.SphereLight):
            light_position = LightingSystem.get_sphere_light_position(light)

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
