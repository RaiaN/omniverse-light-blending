from pxr import UsdLux, Usd
from .light_model import LightModel

__all__ = ["SphereLightModel"]

DEFAULT_DISTANT_LIGHT_RADIUS = 500


class SphereLightModel(LightModel):
    def __init__(self, light):
        super().__init__(light)

        usd_light = UsdLux.Light(light)
        sphere_light = UsdLux.SphereLight(usd_light)
        self._radius = sphere_light.GetRadiusAttr().Get(Usd.TimeCode())

        print("Light radius: ", self._radius)
