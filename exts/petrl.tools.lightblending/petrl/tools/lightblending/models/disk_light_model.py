from .light_model import LightModel
import time

__all__ = ["DiskLightModel"]

CHANGE_LIGHT_INTENSITY_FREQUENCY_SECONDS = 1.5


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

            if self._intensity == 0:
                self._set_intensity(self.get_default_intensity())
            else:
                self._set_intensity(0)

