from .light_model import LightModel
from ..manipulator import SphereLightVisualizer

__all__ = ["DistantLightModel"]

DEFAULT_DISTANT_LIGHT_RADIUS = 500


class DistantLightModel(LightModel):
    def __init__(self, light):
        super().__init__(light)

        self._radius = DEFAULT_DISTANT_LIGHT_RADIUS
        print("Distant Light radius: ", self._radius)

    def update_light_intensity(self, camera_position):
        light_position = self.get_position()
        distance_to_camera = (camera_position - light_position).GetLength()

        if distance_to_camera < self.get_radius():
            self._set_intensity(self.get_default_intensity())
        else:
            self._set_intensity(0)

    def set_radius(self, new_radius):
        # only called by distant light widget
        self._radius = new_radius
        self.mark_as_dirty()

    def on_changed(self, property_name):
        if property_name == "radius":
            self.mark_as_dirty()
        elif "translate" in property_name:
            self.mark_as_dirty()

    # below two methods always go in pair
    def has_visualizer(self):
        return True

    def get_visualizer(self):
        return SphereLightVisualizer(model=self)
