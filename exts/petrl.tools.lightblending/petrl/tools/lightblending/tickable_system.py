import omni.kit.app

__all__ = ["TickableSystem"]


class TickableSystem():
    def startup(self):
        app = omni.kit.app.get_app()

        self._update_end_sub = app.get_update_event_stream().create_subscription_to_pop(
            self._on_update,
            name="LightBlendingTickableSystem"
        )

    def _on_update(self, _):
        print('TickableSystem tick()')
