from .light_model import LightModel

__all__ = ["DistantLightModel"]

DEFAULT_DISTANT_LIGHT_RADIUS = 500


class DistantLightModel(LightModel):
    def __init__(self, light):
        super().__init__(light)

        self._radius = DEFAULT_DISTANT_LIGHT_RADIUS
        print("Light radius: ", self._radius)
