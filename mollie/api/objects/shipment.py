from .base import ObjectBase
from .list import Collection
from .order_line import OrderLine


class Shipment(ObjectBase):
    @property
    def resource(self):
        return self._get_property("resource")

    @property
    def id(self):
        return self._get_property("id")

    @property
    def order_id(self):
        return self._get_property("orderId")

    @property
    def created_at(self):
        return self._get_property("createdAt")

    @property
    def tracking(self):
        return self._get_property("tracking")

    @property
    def tracking_url(self):
        return self.tracking["url"] if self.has_tracking_url() else None

    @property
    def lines(self):
        """Return the order lines of this shipment."""
        lines = self._get_property("lines") or []
        result = {
            "_embedded": {
                "lines": lines,
            },
            "count": len(lines),
        }
        return Collection(result, OrderLine, self.client)

    @property
    def order(self):
        """Return the order of this shipment."""
        return self.client.orders.get(self.order_id)

    # additional methods

    def has_tracking(self):
        return self.tracking is not None

    def has_tracking_url(self):
        return self.has_tracking() and self.tracking["url"] is not None
