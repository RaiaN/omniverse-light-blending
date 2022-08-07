import omni.kit
from pxr import UsdGeom, Gf
from pxr.Usd import TimeCode


__all__ = ["LightUtils"]


class LightUtils:
    @staticmethod
    def get_camera_position():
        viewport_window = omni.kit.viewport_legacy.get_default_viewport_window()
        if not viewport_window:
            return None

        camera_path = viewport_window.get_active_camera()
        if not camera_path:
            return None

        camera_prim = omni.usd.get_context().get_stage().GetPrimAtPath(camera_path)
        # print(camera_prim.GetTypeName())

        camera = UsdGeom.Camera(camera_prim).GetCamera()

        camera_position_world_space = camera.transform.ExtractTranslation()
        return camera_position_world_space

    @staticmethod
    def get_light_position(light):
        light_prim = UsdGeom.Imageable(light)
        _, _, _, position = light_prim.ComputeLocalToWorldTransform(TimeCode())
        position = position[:3]
        position = Gf.Vec3f(position)

        return position
