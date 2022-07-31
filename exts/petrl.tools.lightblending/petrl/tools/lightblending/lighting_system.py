import omni.kit.app
from pxr import UsdLux

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
        # only do light blending with # lights > 1
        # if len(self.tracked_lights) <= 1:
        #     return

        print("Active camera position: ", CameraUtils.GetCameraPosition())
        # todo: calculate distance between lights
        # todo: gradually reduce intensity when camera is moving outside of the light radius and vice versa

    @staticmethod
    def get_instance():
        if LightingSystem.instance is None:
            print("creating new lighting system")
            LightingSystem.instance = LightingSystem()

        return LightingSystem.instance
