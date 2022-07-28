import omni.kit.app
from pxr import UsdLux

from .light_model import LightModel

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

    def add_light(self, light):
        if not light.IsA(UsdLux.Light):
            print('selected primitive is not light: ', light)
            return

        if light not in self.tracked_lights:
            # todo: track lights by path
            self.tracked_lights.append(light)
            self.light_models.append(LightModel(light))

    def remove_light(self, light):
        # todo
        print(light)
        pass

    def _on_update(self, _):
        pass
        # print('TickableSystem tick()')

    @staticmethod
    def get_instance():
        if LightingSystem.instance is None:
            LightingSystem.instance = LightingSystem()
        return LightingSystem.instance
