from omni.ui import scene as sc
from omni.ui import color as cl

__all__ = ["DistantLightManipulator"]

INTENSITY_SCALE = 500.0

ARROW_WIDTH = 0.015
ARROW_HEIGHT = 0.1
ARROW_P = [
    [ARROW_WIDTH, ARROW_WIDTH, 0],
    [-ARROW_WIDTH, ARROW_WIDTH, 0],
    [0, 0, ARROW_HEIGHT],
    #
    [ARROW_WIDTH, -ARROW_WIDTH, 0],
    [-ARROW_WIDTH, -ARROW_WIDTH, 0],
    [0, 0, ARROW_HEIGHT],
    #
    [ARROW_WIDTH, ARROW_WIDTH, 0],
    [ARROW_WIDTH, -ARROW_WIDTH, 0],
    [0, 0, ARROW_HEIGHT],
    #
    [-ARROW_WIDTH, ARROW_WIDTH, 0],
    [-ARROW_WIDTH, -ARROW_WIDTH, 0],
    [0, 0, ARROW_HEIGHT],
    #
    [ARROW_WIDTH, ARROW_WIDTH, 0],
    [-ARROW_WIDTH, ARROW_WIDTH, 0],
    [-ARROW_WIDTH, -ARROW_WIDTH, 0],
    [ARROW_WIDTH, -ARROW_WIDTH, 0],
]

ARROW_VC = [3, 3, 3, 3, 4]
ARROW_VI = [i for i in range(sum(ARROW_VC))]


class DistantLightManipulator(sc.Manipulator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._shape_xform = None

    def __del__(self):
        self.model = None

    def _build_shape(self):
        if not self.model:
            return

        radius = self.model.get_radius()
        # this INTENSITY_SCALE is too make the transform a reasonable length with large intensity number
        z = self.model.get_intensity() / INTENSITY_SCALE
        self._shape_xform.transform = [radius, 0, 0, 0, 0, radius, 0, 0, 0, 0, z, 0, 0, 0, 0, 1]

    def on_build(self):
        """Called when the model is changed and rebuilds the whole slider"""
        model = self.model
        if not model:
            return

        # Style settings, as kwargs
        thickness = 1
        color = cl.yellow
        shape_style = {"thickness": thickness, "color": color}

        def set_thickness(sender, shapes, thickness):
            for shape in shapes:
                shape.thickness = thickness

        self.__root_xf = sc.Transform(model._get_transform())
        # todo: draw sphere
        # todo: take into account light intensity 
        '''with self.__root_xf:
            self._x_xform = sc.Transform()
            with self._x_xform:
                self._shape_xform = sc.Transform()
                # Build the shape's transform
                self._build_shape()
                with self._shape_xform:
                    # Build the shape geomtery as unit-sized
                    h = 0.5
                    z = -1.0

                    # the rectangle
                    shape1 = sc.Sphere((-h, h, 0), (h, h, 0), **shape_style)
                    shape2 = sc.Line((-h, -h, 0), (h, -h, 0), **shape_style)
                    shape3 = sc.Line((h, h, 0), (h, -h, 0), **shape_style)
                    shape4 = sc.Line((-h, h, 0), (-h, -h, 0), **shape_style)

                    # create z-axis to indicate the intensity
                    z1 = sc.Line((h, h, 0), (h, h, z), **shape_style)
                    z2 = sc.Line((-h, -h, 0), (-h, -h, z), **shape_style)
                    z3 = sc.Line((h, -h, 0), (h, -h, z), **shape_style)
                    z4 = sc.Line((-h, h, 0), (-h, h, z), **shape_style)

                    def make_arrow(translate):
                        vert_count = len(ARROW_VI)
                        with sc.Transform(
                            transform=sc.Matrix44.get_translation_matrix(translate[0], translate[1], translate[2])
                            * sc.Matrix44.get_rotation_matrix(0, -180, 0, True)
                        ):
                            return sc.PolygonMesh(ARROW_P, [color] * vert_count, ARROW_VC, ARROW_VI, visible=False)

                    # arrows on the z-axis
                    arrow_1 = make_arrow((h, h, z))
                    arrow_2 = make_arrow((-h, -h, z))
                    arrow_3 = make_arrow((h, -h, z))
                    arrow_4 = make_arrow((-h, h, z))

                    # the line underneath the arrow which is where the gesture applies
                    z1_arrow = sc.Line((h, h, z), (h, h, z - ARROW_HEIGHT), **shape_style)
                    z2_arrow = sc.Line((-h, -h, z), (-h, -h, z - ARROW_HEIGHT), **shape_style)
                    z3_arrow = sc.Line((h, -h, z), (h, -h, z - ARROW_HEIGHT), **shape_style)
                    z4_arrow = sc.Line((-h, h, z), (-h, h, z - ARROW_HEIGHT), **shape_style)

                    def set_visible(sender, shapes, thickness, arrows, visible):
                        set_thickness(sender, shapes, thickness)
                        for arrow in arrows:
                            arrow.visible = visible

                    thickness_group = [z1, z1_arrow, z2, z2_arrow, z3, z3_arrow, z4, z4_arrow]
                    visible_group = [arrow_1, arrow_2, arrow_3, arrow_4]

                    # create 4 rectangles at the corner, and add gesture to update width, height and intensity at the same time
                    s = 0.03

                    def make_corner_rect(translate):
                        with sc.Transform(transform=sc.Matrix44.get_translation_matrix(translate[0], translate[1], translate[2])):
                            return sc.Rectangle(s, s, color=0x0)

                    def set_color_and_visible(sender, shapes, thickness, arrows, visible, rects, color):
                        set_visible(sender, shapes, thickness, arrows, visible)
                        for rect in rects:
                            rect.color = color'''

    def on_model_updated(self, item):
        # todo regenerate the mesh
        '''if not self.model:
            return

        if item == self.model.transform:
            # If transform changed, update the root transform
            self.__root_xf.transform = self.model.get_as_floats(item)
        elif item == self.model.prim_path:
            # If prim_path or width or height or intensity changed, redraw everything
            self.invalidate()
        elif item == self.model.width or item == self.model.height or item == self.model.intensity:
            # Interpret None as changing multiple light shape settings
            self._build_shape()'''
