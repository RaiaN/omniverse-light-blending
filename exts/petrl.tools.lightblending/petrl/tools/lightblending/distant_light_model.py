from .light_model import LightModel

__all__ = ["DistantLightModel"]

DEFAULT_DISTANT_LIGHT_RADIUS = 500


class DistantLightModel(LightModel):
    def __init__(self, light):
        super().__init__(light)

        self._radius = DEFAULT_DISTANT_LIGHT_RADIUS
        print("Light radius: ", self._radius)

    def update_light_intensity(self, camera_position):
        light_position = self.get_position()
        distance_to_camera = (camera_position - light_position).GetLength()

        if distance_to_camera < self.get_radius():
            self._set_intensity(self.get_default_intensity())
        else:
            self._set_intensity(0)
