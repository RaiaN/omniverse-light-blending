from omni.ui import scene as sc

__all__ = ["LightManipulator"]


class LightManipulator(sc.Manipulator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._visualizer = None
        self._enabled = True

    def __del__(self):
        if self.model:
            self.model.set_on_model_dirty_event(None)
            self.model = None

        self._visualizer = None

    def set_model(self, model):
        if self.model:
            self.model.set_on_model_dirty_event(None)

        self.model = model

        if self.model:
            self.model.set_on_model_dirty_event(self.on_draw_event)
            self._visualizer = self.model.get_visualizer()
        else:
            self._visualizer = None

        self.on_draw_event(True)

    def on_draw_event(self, enabled):
        self._enabled = enabled
        self.invalidate()

    def on_build(self):
        """Called when the model is changed and rebuilds the whole slider"""
        model = self.model
        if not model or not self._enabled:
            return

        # print("On build!")

        if self._visualizer:
            self._visualizer.visualize()
