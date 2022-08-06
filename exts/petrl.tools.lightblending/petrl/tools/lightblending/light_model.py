import omni.usd
from pxr import UsdLux, Usd, Gf
from omni.ui import scene as sc
from .utils import LightUtils

__all__ = ["LightModel"]


def _flatten_matrix(matrix: Gf.Matrix4d):
    m0, m1, m2, m3 = matrix[0], matrix[1], matrix[2], matrix[3]
    return [
        m0[0],
        m0[1],
        m0[2],
        m0[3],
        m1[0],
        m1[1],
        m1[2],
        m1[3],
        m2[0],
        m2[1],
        m2[2],
        m2[3],
        m3[0],
        m3[1],
        m3[2],
        m3[3],
    ]


class LightModel(sc.AbstractManipulatorModel):
    def __init__(self, light):
        super().__init__()

        self._on_draw_event = None

        usd_light = UsdLux.Light(light)

        self._light_path = usd_light.GetPrim().GetPath().pathString
        print("Light path: ", self._light_path)

        self._intensity = usd_light.GetIntensityAttr().Get()
        self._default_intensity = self._intensity
        print("Light intensity (current): ", self._intensity)

        sphere_light = UsdLux.SphereLight(usd_light)
        distant_light = UsdLux.DistantLight(usd_light)
        if sphere_light:
            self._radius = sphere_light.GetRadiusAttr().Get(Usd.TimeCode())
        elif distant_light:
            # todo: define proper default radius for distant light
            self._radius = 500

        print("Light radius: ", self._radius)

        # Listen for object selection changes
        self._events = self._usd_context.get_stage_event_stream()
        self._stage_event_sub = self._events.create_subscription_to_pop(
            self._on_stage_event, name="Light Manipulator Selection Change"
        )

    def cleanup_listeners(self):
        print("Cleaning up stage listeners")

        if hasattr(self, "_stage_listener") and self._stage_listener:
            print("Unregistered stage listener for light: ", self._light_path)
            self._stage_listener.Revoke()
            self._stage_listener = None

        self.set_intensity(self._default_intensity)

    @property
    def _usd_context(self) -> Usd.Stage:
        # Get the UsdContext we are attached to
        return omni.usd.get_context()

    def get_default_intensity(self):
        return self._default_intensity

    def get_intensity(self):
        return self._intensity

    def get_radius(self):
        return self._radius

    def get_light(self):
        stage = self._usd_context.get_stage()
        prim = stage.GetPrimAtPath(self._light_path)
        return UsdLux.Light(prim)

    def get_transform(self):
        light = self.get_light()

        # Compute matrix from world-transform in USD
        world_xform = light.ComputeLocalToWorldTransform(Usd.TimeCode())

        # Flatten Gf.Matrix4d to list
        return _flatten_matrix(world_xform)

    def get_position(self):
        light = self.get_light()
        return LightUtils.get_light_position(light)

    def set_intensity(self, new_intensity):
        light = self.get_light()

        light.GetIntensityAttr().Set(new_intensity, Usd.TimeCode())
        self._intensity = new_intensity

    def set_on_draw_event(self, event):
        self._on_draw_event = event

    def _on_stage_event(self, event):
        """Called by stage_event_stream"""
        if event.type == int(omni.usd.StageEventType.SELECTION_CHANGED):
            self._on_kit_selection_changed()

    def _on_kit_selection_changed(self):
        usd_context = self._usd_context
        if not usd_context:
            return

        stage = usd_context.get_stage()
        if not stage:
            return

        prim_paths = usd_context.get_selection().get_selected_prim_paths() if usd_context else None
        if not prim_paths:
            return

        if prim_paths[0] == self._light_path:
            print("Selected light: ", self._light_path)
            if self._on_draw_event:
                self._on_draw_event(True)
        else:
            if self._on_draw_event:
                self._on_draw_event(False)

        # Add a Tf.Notice listener to update the light attributes
        stage = self._usd_context.get_stage()
        # if not hasattr(self, "_stage_listener"):
        #     print("Registered stage listener for light: ", self._light_path)
        #     self._stage_listener = Tf.Notice.Register(Usd.Notice.ObjectsChanged, self._notice_changed, stage)

    def _notice_changed(self, notice, stage):
        """Called by Tf.Notice. When USD data changes, we update light model"""

        changed_items = set()

        # changed_items = set()
        for p in notice.GetChangedInfoOnlyPaths():
            prim_path = p.GetPrimPath().pathString

            if prim_path != self._light_path:
                continue

            if p.name == "intensity":
                prim = stage.GetPrimAtPath(prim_path)
                usd_light = UsdLux.Light(prim)

                print("Light intensity changed for object: ", usd_light)

                if self._on_draw_event:
                    self._on_draw_event()

                # self._intensity = usd_light.GetIntensityAttr().Get()
                # changed_items.add(self._intensity)

                # print("Light intensity changed to: ", self._intensity)
            elif p.name == "radius":
                if self._on_draw_event:
                    self._on_draw_event()

            # todo: how to handle radius changes for distant light?
            # todo: use custom widget to set radius for distant light?

        for item in changed_items:
            self._item_changed(item)
