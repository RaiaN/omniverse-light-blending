from omni.ui import scene as sc

from .distant_light_visualizer import DistantLightVisualizer

__all__ = ["ViewportScene"]


class ViewportScene:
    """The light Manipulator, placed into a Viewport"""

    def __init__(self, viewport_window, ext_id: str):
        self._scene_view = None
        self._viewport_window = viewport_window

        # Create a unique frame for our SceneView
        with self._viewport_window.get_frame(ext_id):
            # Create a default SceneView (it has a default camera-model)
            self._scene_view = sc.SceneView()

            with self._scene_view.scene:
                self._visualizer = DistantLightVisualizer()

            # Register the SceneView with the Viewport to get projection and view updates
            self._viewport_window.viewport_api.add_scene_view(self._scene_view)

    def __del__(self):
        self.destroy()

    def destroy(self):
        if self._scene_view:
            # Empty the SceneView of any elements it may have
            self._scene_view.scene.clear()
            # Be a good citizen, and un-register the SceneView from Viewport updates
            if self._viewport_window:
                self._viewport_window.viewport_api.remove_scene_view(self._scene_view)

        # Remove our references to these objects
        self._viewport_window = None
        self._scene_view = None

    def set_light_model(self, model):
        self._visualizer.set_model(model)
