from pxr import UsdLux
from .distant_light_model import DistantLightModel
from .sphere_light_model import SphereLightModel
from .disk_light_model import DiskLightModel

__all__ = ["LightModelFactory"]


class LightModelFactory:
    @staticmethod
    def new_model(light):
        model = None
        if light.IsA(UsdLux.DistantLight):
            model = DistantLightModel(light)
        elif light.IsA(UsdLux.SphereLight):
            model = SphereLightModel(light)
        elif light.IsA(UsdLux.DiskLight):
            model = DiskLightModel(light)

        return model
