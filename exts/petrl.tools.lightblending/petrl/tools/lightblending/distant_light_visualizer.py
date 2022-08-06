from omni.ui import scene as sc
from omni.ui import color as cl

__all__ = ["DistantLightVisualizer"]


class DistantLightVisualizer(sc.Manipulator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

    def on_model_updated(self, item):
        # Regenerate the mesh
        self.invalidate()
