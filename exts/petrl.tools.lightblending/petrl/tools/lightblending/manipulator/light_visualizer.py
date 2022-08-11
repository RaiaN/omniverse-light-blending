from omni.ui import color as cl

__all__ = ["LightVisualizer"]


class LightVisualizer:
    def __init__(self, model, color=None):
        self.model = model
        self.color = cl.blue if color is None else color

    def __del__(self):
        pass

    def visualize(self):
        pass
