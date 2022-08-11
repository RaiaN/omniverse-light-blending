from .light_model import LightModel
import time

__all__ = ["DiskLightModel"]

CHANGE_LIGHT_INTENSITY_FREQUENCY_SECONDS = 1.25


class DiskLightModel(LightModel):
    def __init__(self, light):
        super().__init__(light)

        self._time_prev = time.time()

        # disk light is visible everywhere
        self._radius = 99999999999
        print("Light radius: ", self._radius)

    def update_light_intensity(self, camera_position):
        time_now = time.time()
        if time_now - self._time_prev >= CHANGE_LIGHT_INTENSITY_FREQUENCY_SECONDS:
            self._time_prev = time_now

            light_position = self.get_position()
            distance_to_camera = (camera_position - light_position).GetLength()
            light_is_active = distance_to_camera < self.get_radius()

            if self._intensity == 0 and light_is_active:
                self._set_intensity(self.get_default_intensity())
            else:
                self._set_intensity(0)
