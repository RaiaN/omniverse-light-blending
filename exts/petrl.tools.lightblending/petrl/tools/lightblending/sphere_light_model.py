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

    def update_light_intensity(self, camera_position):
        light_position = self.get_position()
        distance_to_camera = (camera_position - light_position).GetLength()
        light_weight = float(distance_to_camera / (self.get_radius() + 0.0001))
        # print("Light weight: ", light_weight)

        new_intensity = 1.0 - min(1.0, light_weight)
        # print(new_intensity)
        new_intensity = new_intensity * self.get_default_intensity()
        # print(new_intensity)
        # print("New intensity: ", new_intensity)

        self._set_intensity(new_intensity)
