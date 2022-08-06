import omni.usd
from pxr import UsdLux, Usd, Tf
from omni.ui import scene as sc
from .utils import LightUtils

__all__ = ["LightModel"]

DEFAULT_DISTANT_LIGHT_RADIUS = 500


class LightModel(sc.AbstractManipulatorModel):
    def __init__(self, light):
        super().__init__()

        self._on_draw_event = None
        self._stage_listener = None

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
            self._radius = DEFAULT_DISTANT_LIGHT_RADIUS

        print("Light radius: ", self._radius)

        # Listen for object selection changes
        self._events = self._usd_context.get_stage_event_stream()
        self._stage_event_sub = self._events.create_subscription_to_pop(
            self._on_stage_event, name="Light Manipulator Selection Change"
        )

    def cleanup_listeners(self):
        print("Cleaning up stage listeners")

        if self._stage_listener:
            print("Unregistered stage listener for light: ", self._light_path)
            self._stage_listener.Revoke()
            self._stage_listener = None

        self.set_intensity(self._default_intensity)

    @property
    def _usd_context(self) -> Usd.Stage:
        # Get the UsdContext we are attached to
        return omni.usd.get_context()

    def get_light_path(self):
        return self._light_path

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

    def get_position(self):
        light = self.get_light()
        return LightUtils.get_light_position(light)

    def set_intensity(self, new_intensity):
        light = self.get_light()

        light.GetIntensityAttr().Set(new_intensity, Usd.TimeCode())
        self._intensity = new_intensity

    def set_radius(self, new_radius):
        # only called by distant light widget
        self._radius = new_radius
        self._on_draw_event(True)

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
            if self._stage_listener:
                self._stage_listener.Revoke()
                self._stage_listener = None

            if self._on_draw_event:
                self._on_draw_event(False)

        # Add a Tf.Notice listener to update the light attributes
        if self._stage_listener is None:
            print("Registered stage listener for light: ", self._light_path)

            stage = self._usd_context.get_stage()
            self._stage_listener = Tf.Notice.Register(Usd.Notice.ObjectsChanged, self._notice_changed, stage)

    def _notice_changed(self, notice, stage):
        """Called by Tf.Notice. When USD data changes, we update light model"""

        changed_items = set()

        for p in notice.GetChangedInfoOnlyPaths():
            prim_path = p.GetPrimPath().pathString

            if prim_path != self._light_path:
                continue

            print("Attribute changed: ", p.name)

            if p.name == "intensity":
                prim = stage.GetPrimAtPath(prim_path)
                usd_light = UsdLux.Light(prim)

                print("Light intensity changed for object: ", usd_light)

                # self._intensity = usd_light.GetIntensityAttr().Get()
                # changed_items.add(self._intensity)

                # print("Light intensity changed to: ", self._intensity)
            elif p.name == "radius":
                if self._on_draw_event:
                    self._on_draw_event(True)
            elif "translate" in p.name:
                if self._on_draw_event:
                    self._on_draw_event(True)

        for item in changed_items:
            self._item_changed(item)
