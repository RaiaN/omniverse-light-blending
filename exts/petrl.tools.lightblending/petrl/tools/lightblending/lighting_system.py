import omni.kit.app
from pxr import UsdLux, UsdGeom
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
        print(light)
        pass

    def _on_update(self, _):
        camera_position = CameraUtils.GetCameraPosition()
        # print("Active camera position: ", camera_position)

        for light in self.tracked_lights:
            light_prim = UsdGeom.Imageable(light)
            _, _, _, position = light_prim.ComputeLocalToWorldTransform(TimeCode())
            position = position[:3]
            print("Light position: ", light, position)

        # todo: calculate distance between lights
        # todo: gradually reduce intensity to 0.0 when camera is moving outside of the light radius and vice versa

    @staticmethod
    def get_instance():
        if LightingSystem.instance is None:
            print("creating new lighting system")
            LightingSystem.instance = LightingSystem()

        return LightingSystem.instance
