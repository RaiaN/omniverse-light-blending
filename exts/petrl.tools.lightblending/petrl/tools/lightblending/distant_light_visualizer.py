import omni.ui as ui
from omni.ui import scene as sc
from omni.ui import color as cl

__all__ = ["DistantLightVisualizer"]


class DistantLightVisualizer(sc.Manipulator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._root = None
        self._name_label = None
        self._enabled = True

    def __del__(self):
        self.model = None

    def set_model(self, model):
        if self.model:
            self.model.set_on_draw_event(None)

        self.model = model
        self.model.set_on_draw_event(self.on_draw_event)

    def on_draw_event(self, enabled):
        self._enabled = enabled
        self.invalidate()

    def on_build(self):
        """Called when the model is changed and rebuilds the whole slider"""
        model = self.model
        if not model or not self._enabled:
            return

        radius = self.model.get_radius()

        position = self.model.get_position()

        with sc.Transform(transform=sc.Matrix44.get_translation_matrix(*position)):
            with sc.Transform(look_at=sc.Transform.LookAt.CAMERA):
                sc.Arc(radius, axis=2, color=cl.yellow, wireframe=True)
                sc.Arc(radius, axis=1, color=cl.yellow, wireframe=True)
                sc.Arc(radius, axis=0, color=cl.yellow, wireframe=True)

        # show widget
        if self._root:
            self._root.transform = sc.Matrix44.get_translation_matrix(*position)
            self._root.visible = True

        # update light name
        if self._name_label:
            self._name_label.text = f"Light:{self.model.get_light_path()}"

        self._root = sc.Transform(visible=False)
        with self._root:
            with sc.Transform(scale_to=sc.Space.SCREEN):
                with sc.Transform(transform=sc.Matrix44.get_translation_matrix(0, 100, 0)):
                    self._widget = sc.Widget(500, 150, update_policy=sc.Widget.UpdatePolicy.ON_MOUSE_HOVERED)
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
