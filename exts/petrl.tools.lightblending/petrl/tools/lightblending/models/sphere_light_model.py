from .light_model import LightModel
from ..manipulator import SphereLightVisualizer

__all__ = ["SphereLightModel"]

DEFAULT_SPHERE_LIGHT_RADIUS = 400
CUTOFF_DISTANCE = 200


class SphereLightModel(LightModel):
    def __init__(self, light):
        super().__init__(light)

        self._radius = DEFAULT_SPHERE_LIGHT_RADIUS

        print("Sphere Light radius: ", self._radius)

    def update_light_intensity(self, camera_position):
        light_position = self.get_position()
        distance_to_camera = (camera_position - light_position).GetLength()
        distance_to_camera = max(distance_to_camera - CUTOFF_DISTANCE, 0)

        light_weight = float(distance_to_camera / (self.get_radius() + 0.0001))
        # print("Light weight: ", light_weight)

        new_intensity = 1.0 - min(1.0, light_weight)
        # print(new_intensity)
        new_intensity = new_intensity * self.get_default_intensity()
        # print(new_intensity)
        # print("New intensity: ", new_intensity)

        self._set_intensity(new_intensity)

    def set_radius(self, new_radius):
        # only called by sphere light widget
        self._radius = new_radius
        self.mark_as_dirty()

    def has_visualizer(self):
        # override if model has a visualizer
        return True

    def get_visualizer(self):
        return SphereLightVisualizer(model=self)
