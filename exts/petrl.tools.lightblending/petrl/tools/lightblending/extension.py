import omni.ext
from .context_menu import LightBlendingContextMenu
from .lighting_system import LightingSystem

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.


class MyExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[petrl.tools.lightblending] MyExtension startup")

        self.light_system = LightingSystem.get_instance()
        self.light_system.startup()

        self.context_menu = LightBlendingContextMenu()
        self.context_menu.on_startup()

        # self._editor_menu = ui

    def on_shutdown(self):
        print("[petrl.tools.lightblending] MyExtension shutdown")
        self.light_system = None
        self.context_menu.on_shutdown()
