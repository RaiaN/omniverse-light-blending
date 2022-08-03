import omni.ext
from omni.kit.viewport.utility import get_active_viewport_window
from .context_menu import LightBlendingContextMenu
from .lighting_system import LightingSystem
from .viewport_scene import ViewportScene


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.


class MyExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[petrl.tools.lightblending] MyExtension startup")

        viewport_window = get_active_viewport_window()

        # Build out the scene
        self._viewport_scene = ViewportScene(viewport_window, ext_id)

        self.light_system = LightingSystem.get_instance()
        self.light_system.startup(self._viewport_scene)

        self.context_menu = LightBlendingContextMenu()
        self.context_menu.on_startup()

    def on_shutdown(self):
        print("[petrl.tools.lightblending] MyExtension shutdown")
        self._viewport_scene.destroy()
        self._viewport_scene = None

        self.light_system.shutdown()
        self.context_menu.on_shutdown()
