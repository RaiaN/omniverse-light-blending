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
            name="LightBlendingTickableSystem"
        )

        self.tracked_lights = []
        self.light_models = []

    def shutdown(self):
        for model in self.light_models:
            if model:
                print("Cleaning up light model: ", model)
                model.cleanup_listeners()

        if hasattr(self, "_update_end_sub") and self._update_end_sub is not None:
            print("Unsubscribe from update event stream")
            self._update_end_sub.unsubscribe()

        self.tracked_lights = []
        self.light_models = []

    def add_light(self, light):
        if not light.IsA(UsdLux.Light):
            print('selected primitive is not light: ', light)
            return

        if light not in self.tracked_lights:
            print("Adding light: ", light)
            # todo: track lights by path
            self.tracked_lights.append(light)
            self.light_models.append(LightModel(light))

            print("Tracked lights: ", self.tracked_lights)
        else:
            print("Light is already being tracked!")

    def remove_light(self, light):
        # todo
        # print(light)
        pass

    def _on_update(self, args):
        print(args)

        camera_position = Gf.Vec3f(CameraUtils.GetCameraPosition())
        # print("Active camera position: ", camera_position)

        try:
            for light, light_model in zip(self.tracked_lights, self.light_models):
                light_prim = UsdGeom.Imageable(light)
                _, _, _, position = light_prim.ComputeLocalToWorldTransform(TimeCode())
                position = position[:3]
                position = Gf.Vec3f(position)

                distance = (camera_position - position).GetLength()

                light_weight = float(distance / (light_model.get_radius() + 0.0001))
                # print("Light weight: ", light_weight)

                new_intensity = 1.0 - min(1.0, light_weight)
                # print(new_intensity)
                new_intensity = new_intensity * light_model.get_default_intensity()
                # print(new_intensity)
                # print("New intensity: ", new_intensity)

                light_model.set_intensity(new_intensity)
        except Exception as exc:
            print("Exception: ", exc)

        # todo: gradually reduce intensity to 0.0 when camera is moving outside of the light radius and vice versa

    @staticmethod
    def get_instance():
        if LightingSystem.instance is None:
            # print("creating new lighting system")
            LightingSystem.instance = LightingSystem()

        return LightingSystem.instance
