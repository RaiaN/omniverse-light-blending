import omni.ui as ui
from omni.ui import scene as sc
from omni.ui import color as cl
from .light_visualizer import LightVisualizer

__all__ = ["DistantLightVisualizer"]


class _ViewportLegacyDisableSelection:
    """Disables selection in the Viewport Legacy"""

    def __init__(self):
        self._focused_windows = None
        focused_windows = []
        try:
            # For some reason is_focused may return False, when a Window is definitely in fact is the focused window!
            # And there's no good solution to this when mutliple Viewport-1 instances are open; so we just have to
            # operate on all Viewports for a given usd_context.
            import omni.kit.viewport_legacy as vp

            vpi = vp.acquire_viewport_interface()
            for instance in vpi.get_instance_list():
                window = vpi.get_viewport_window(instance)
                if not window:
                    continue
                focused_windows.append(window)
            if focused_windows:
                self._focused_windows = focused_windows
                for window in self._focused_windows:
                    # Disable the selection_rect, but enable_picking for snapping
                    window.disable_selection_rect(True)
        except Exception:
            pass


class _DragPrioritize(sc.GestureManager):
    """Refuses preventing _DragGesture."""

    def can_be_prevented(self, gesture):
        # Never prevent in the middle of drag
        return gesture.state != sc.GestureState.CHANGED

    def should_prevent(self, gesture, preventer):
        if preventer.state == sc.GestureState.BEGAN or preventer.state == sc.GestureState.CHANGED:
            return True


class _DragGesture(sc.DragGesture):
    """"Gesture to disable rectangle selection in the viewport legacy"""

    def __init__(self):
        super().__init__(manager=_DragPrioritize())

    def on_began(self):
        # When the user drags the slider, we don't want to see the selection
        # rect. In Viewport Next, it works well automatically because the
        # selection rect is a manipulator with its gesture, and we add the
        # slider manipulator to the same SceneView.
        # In Viewport Legacy, the selection rect is not a manipulator. Thus it's
        # not disabled automatically, and we need to disable it with the code.
        self.__disable_selection = _ViewportLegacyDisableSelection()

    def on_ended(self):
        # This re-enables the selection in the Viewport Legacy
        self.__disable_selection = None


class DistantLightVisualizer(LightVisualizer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._radius_model = None
        self._radius_subscription = None

    def __del__(self):
        self._radius_subscription = None
        self._radius_model = None

    def visualize(self):
        print("Visualize distant light")

        radius = self.model.get_radius()
        position = self.model.get_position()

        with sc.Transform(transform=sc.Matrix44.get_translation_matrix(*position)):
            with sc.Transform(look_at=sc.Transform.LookAt.CAMERA):
                sc.Arc(radius, axis=2, color=cl.yellow, wireframe=True)
                sc.Arc(radius, axis=1, color=cl.yellow, wireframe=True)
                sc.Arc(radius, axis=0, color=cl.yellow, wireframe=True)

        with sc.Transform(transform=sc.Matrix44.get_translation_matrix(*position)):
            with sc.Transform(look_at=sc.Transform.LookAt.CAMERA):
                with sc.Transform(scale_to=sc.Space.SCREEN):
                    with sc.Transform(transform=sc.Matrix44.get_translation_matrix(0, 100, -300)):
                        self._widget = sc.Widget(500, 200, update_policy=sc.Widget.UpdatePolicy.ON_MOUSE_HOVERED)
                        self._widget.frame.set_build_fn(self.on_build_widgets)

    def on_build_widgets(self):
        with ui.ZStack():
            ui.Rectangle(style={
                "background_color": cl(0.2),
                "border_color": cl(0.7),
                "border_width": 2,
                "border_radius": 4,
            })
            self._name_label = ui.Label("", height=0, alignment=ui.Alignment.CENTER)
            self._name_label.text = f"Light:{self.model.get_light_path()}"

            # setup some model, just for simple demonstration here
            self._radius_model = ui.SimpleIntModel(self.model.get_radius())
            # self._radius_model.as_int = 1
            self._radius_model.set_min(1)
            self._radius_model.set_max(10000)

            ui.Spacer(height=20)
            with ui.HStack():
                ui.Spacer(width=10)
                ui.Label("Radius", height=0, width=0)
                ui.Spacer(width=5)
                ui.IntSlider(self._radius_model, min=1, max=10000, height=10)
                ui.Spacer(width=10)
            ui.Spacer(height=4)
            ui.Spacer()

            # Update the slider
            def update_radius(prim_name, value):
                print(f"Changing radius of {prim_name} to: {value}")
                self.model.set_radius(value)

            if self._radius_model:
                self._radius_subscription = None
                self._radius_subscription = self._radius_model.subscribe_value_changed_fn(
                    lambda m, p=self.model.get_light_path(): update_radius(p, m.as_int)
                )

        self._widget.gestures += [_DragGesture()]
