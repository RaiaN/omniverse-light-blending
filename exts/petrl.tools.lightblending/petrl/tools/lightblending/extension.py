import omni.ext
from .tickable_system import TickableSystem

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.


class MyExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[petrl.tools.lightblending] MyExtension startup")

        self.tickable_system = TickableSystem()
        self.tickable_system.startup()

    def on_shutdown(self):
        print("[petrl.tools.lightblending] MyExtension shutdown")
        self.tickable_system = None
