import omni.kit as kit
import omni.usd as usd

from .lighting_system import LightingSystem

from pxr import UsdLux

__all__ = ["LightBlendingContextMenu"]


class LightBlendingContextMenu:
    def on_startup(self):
        menu = [
            {
                "name": "Light Blending Tools",
                "show_fn": LightBlendingContextMenu.show_fn
            },
            {
                "name": "Add Control Light",
                "onclick_fn": LightBlendingContextMenu.add_light,
                "show_fn": LightBlendingContextMenu.show_add_fn
            },
            {
                "name": "Remove Control Light",
                "onclick_fn": LightBlendingContextMenu.remove_light,
                "show_fn": LightBlendingContextMenu.show_remove_fn
            }
        ]
        # add to all context menus
        self._my_custom_menu = kit.context_menu.add_menu(menu, "MENU", "")

    def on_shutdown(self):
        # remove event
        self._stage_event_sub = None
        self._my_custom_menu = None

    def add_light(objects):
        if 'prim_list' in objects:
            for light in objects['prim_list']:
                LightingSystem.get_instance().add_light(light)
                break

    def remove_light(objects):
        if 'prim_list' in objects:
            for light in objects['prim_list']:
                LightingSystem.get_instance().remove_light(light)
                break

    def show_fn(objects: dict):
        return LightBlendingContextMenu.show_add_fn(objects) or LightBlendingContextMenu.show_remove_fn(objects)

    def show_add_fn(objects: dict):
        usd_context = usd.get_context()
        stage = usd_context.get_stage()

        prim_paths = usd_context.get_selection().get_selected_prim_paths()

        if len(prim_paths) > 0:
            prim = stage.GetPrimAtPath(prim_paths[0])
            if prim.IsA(UsdLux.Light):
                return not LightingSystem.get_instance().has_light(prim)

        return False

    def show_remove_fn(objects: dict):
        usd_context = usd.get_context()
        stage = usd_context.get_stage()

        prim_paths = usd_context.get_selection().get_selected_prim_paths()

        if len(prim_paths) > 0:
            prim = stage.GetPrimAtPath(prim_paths[0])
            if prim.IsA(UsdLux.Light):
                return LightingSystem.get_instance().has_light(prim)

        return False
