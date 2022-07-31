import omni.kit
from pxr import UsdGeom


__all__ = ["CameraUtils"]


class CameraUtils:
    @staticmethod
    def GetCameraPosition():
        viewport_window = omni.kit.viewport_legacy.get_default_viewport_window()

        camera_path = viewport_window.get_active_camera()
        camera_prim = omni.usd.get_context().get_stage().GetPrimAtPath(camera_path)
        # print(camera_prim.GetTypeName())

        camera = UsdGeom.Camera(camera_prim).GetCamera()

        camera_position_world_space = camera.transform.ExtractTranslation()
        return camera_position_world_space
