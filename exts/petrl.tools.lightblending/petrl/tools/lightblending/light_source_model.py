from pxr import UsdLux

__all__ = ["LightSourceModel"]


class LightSourceModel:
    def init(self, light):
        # todo: copy light attributes using GetSchemaAttributeNames

        attributes = UsdLux.Tokens()
        # omni.usd.UsdLux
