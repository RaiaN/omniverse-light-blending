import omni.usd
from pxr import UsdLux, Usd
from omni.ui import scene as sc
from .utils import LightUtils

__all__ = ["LightModel"]


class LightModel(sc.AbstractManipulatorModel):
    def __init__(self, light):
        super().__init__()

        self._on_model_dirty_event = None

        usd_light = UsdLux.Light(light)

        self._light_path = usd_light.GetPrim().GetPath().pathString
        print("Light path: ", self._light_path)

        self._intensity = usd_light.GetIntensityAttr().Get()
        self._default_intensity = self._intensity
        print("Light intensity (current): ", self._intensity)

    def on_shutdown(self):
        self._on_model_dirty_event = None
        self._set_intensity(self._default_intensity)

    def set_on_model_dirty_event(self, event):
        self._on_model_dirty_event = event

    def mark_as_dirty(self):
        if self._on_model_dirty_event:
            self._on_model_dirty_event(True)

    @property
    def _usd_context(self) -> Usd.Stage:
        # Get the UsdContext we are attached to
        return omni.usd.get_context()

    def get_light_path(self):
        return self._light_path

    def get_default_intensity(self):
        return self._default_intensity

    def get_radius(self):
        return self._radius

    def get_light(self):
        stage = self._usd_context.get_stage()
        prim = stage.GetPrimAtPath(self._light_path)
        return UsdLux.Light(prim)

    def get_position(self):
        light = self.get_light()
        return LightUtils.get_light_position(light)

    def set_radius(self, new_radius):
        # only called by distant light widget
        self._radius = new_radius
        # self.mark_as_dirty()

    def _set_intensity(self, new_intensity):
        light = self.get_light()

        # print(light.GetIntensityAttr().GetVariability())

        light.GetIntensityAttr().Set(new_intensity, Usd.TimeCode.Default())
        self._intensity = new_intensity

    def update_light_intensity(self, camera_position):
        raise NotImplementedError("Implement this method for classes that inherit LightModel")
