from omni.ui import scene as sc
from omni.ui import color as cl

__all__ = ["DistantLightVisualizer"]


class DistantLightVisualizer():
    def __init__(self):
        self.model = None
        self._shape_xform = None

    def __del__(self):
        self.model = None

    def set_model(self, model):
        if self.model:
            self.model.set_on_draw_event(None)

        self.model = model
        self.model.set_on_draw_event(self.on_draw_event)

    def on_draw_event(self):
        print("Visualize distant light")
        self.on_build()

    def on_build(self):
        """Called when the model is changed and rebuilds the whole slider"""
        model = self.model
        if not model:
            return

        # Style settings, as kwargs
        thickness = 4
        color = cl.yellow
        shape_style = {"thickness": thickness, "color": color}

        position = self.model.get_position()
        print("Light position: ", position)

        print("Drawing sphere")
        # todo: draw sphere
        # todo: take into account light intensity
        with sc.Transform(transform=sc.Matrix44.get_translation_matrix(*position)):
            # the sphere
            print("Drawing cube")
            sc.Line([-1, -1, -1], [1, -1, -1])
            sc.Line([-1, 1, -1], [1, 1, -1])
            sc.Line([-1, -1, 1], [1, -1, 1])
            sc.Line([-1, 1, 1], [1, 1, 1])

            sc.Line([-1, -1, -1], [-1, 1, -1])
            sc.Line([1, -1, -1], [1, 1, -1])
            sc.Line([-1, -1, 1], [-1, 1, 1])
            sc.Line([1, -1, 1], [1, 1, 1])

            sc.Line([-1, -1, -1], [-1, -1, 1])
            sc.Line([-1, 1, -1], [-1, 1, 1])
            sc.Line([1, -1, -1], [1, -1, 1])
            sc.Line([1, 1, -1], [1, 1, 1])
