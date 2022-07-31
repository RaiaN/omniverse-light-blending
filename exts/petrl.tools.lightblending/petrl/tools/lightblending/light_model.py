from pxr import UsdLux, Tf, Usd
import omni.usd

__all__ = ["LightModel"]


class LightModel:
    def __init__(self, light):
        # todo: establish live updates
        usd_light = UsdLux.Light(light)

        self._light_path = usd_light.GetPrim().GetPath().pathString
        print("Light path: ", self._light_path)

        self._intensity = usd_light.GetIntensityAttr().Get()
        self._default_intensity = self._intensity
        print("Light intensity (current): ", self._intensity)
        print("Light intensity (default): ", self._default_intensity)

        sphere_light = UsdLux.SphereLight(usd_light)
        self._radius = sphere_light.GetRadiusAttr().Get(Usd.TimeCode())
        print("Light radius: ", self._radius)

        # Add a Tf.Notice listener to update the light attributes
        stage = self._usd_context.get_stage()
        if not hasattr(self, "_stage_listener"):
            print("Registered stage listener for light: ", self)
            self._stage_listener = Tf.Notice.Register(Usd.Notice.ObjectsChanged, self._notice_changed, stage)

    def cleanup_listeners(self):
        print("Cleaning up stage listeners")
        if hasattr(self, "_stage_listener") and self._stage_listener:
            print("Unregistered stage listener for light: ", self)
            self._stage_listener.Revoke()
            self._stage_listener = None

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

    def set_intensity(self, new_intensity):
        stage = self._usd_context.get_stage()
        prim = stage.GetPrimAtPath(self._light_path)
        usd_light = UsdLux.Light(prim)

        usd_light.GetIntensityAttr().Set(new_intensity, Usd.TimeCode())
        self._intensity = new_intensity

    def _notice_changed(self, notice, stage):
        """Called by Tf.Notice. When USD data changes, we update light model"""

        # changed_items = set()
        for p in notice.GetChangedInfoOnlyPaths():
            prim_path = p.GetPrimPath().pathString

            if prim_path != self._light_path:
                continue

            if p.name == "intensity":
                prim = stage.GetPrimAtPath(prim_path)
                usd_light = UsdLux.Light(prim)

                print("Light intensity changed for object: ", usd_light)

                self._intensity = UsdLux.Light.GetIntensityAttr(usd_light).Get()

                print("Light intensity changed to: ", self._intensity)

            # todo: listen for 'radius' changes

        # for item in changed_items:
        #     self._item_changed(item)
