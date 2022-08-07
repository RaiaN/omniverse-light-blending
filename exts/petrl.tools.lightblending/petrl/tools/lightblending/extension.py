import carb
import omni.ext
import omni.usd
from omni.kit.viewport.utility import get_active_viewport_window
from .context_menu import LightBlendingContextMenu
from .lighting_system import LightingSystem
from .viewport_scene import ViewportScene


class LightBlendingExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("[petrl.tools.lightblending] LightBlendingExtension startup")

        viewport_window = get_active_viewport_window()
        # Issue an error if there is no Viewport
        if not viewport_window:
            carb.log_error(f"No Viewport Window to add {ext_id} scene to")
            return

        print("Active viewport window: ", viewport_window)

        # Build out the scene
        self._viewport_scene = ViewportScene(viewport_window, ext_id)

        self.light_system = LightingSystem.get_instance()
        self.light_system.startup(self._viewport_scene)

        self.context_menu = LightBlendingContextMenu()
        self.context_menu.on_startup()

        # Listen for object selection changes
        self._events = omni.usd.get_context().get_stage_event_stream()
        self._stage_event_sub = self._events.create_subscription_to_pop(
            self._on_stage_event, name="Stage Events Handler"
        )

    def on_shutdown(self):
        print("[petrl.tools.lightblending] LightBlendingExtension shutdown")
        if self._viewport_scene:
            self._viewport_scene.destroy()
            self._viewport_scene = None

        if self.light_system:
            self.light_system.shutdown()
            self.light_system = None

        if self.context_menu:
            self.context_menu.on_shutdown()
            self.context_menu = None

        if self._stage_event_sub:
            self._stage_event_sub.unsubscribe()
            self._stage_event_sub = None

        LightingSystem.instance = None

    def _on_stage_event(self, event):
        # print("stage event: ", event.type)

        """Called by stage_event_stream"""
        if event.type == int(omni.usd.StageEventType.CLOSING) or event.type == int(omni.usd.StageEventType.CLOSED):
            print("Stage being closed")
            self.light_system.on_stage_changed()
