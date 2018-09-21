from .base import Base
from .list import List
from .order_line import OrderLine


class Shipment(Base):
    @property
    def resource(self):
        return self._get_property('resource')

    @property
    def id(self):
        return self._get_property('id')

    @property
    def order_id(self):
        return self._get_property('orderId')

    @property
    def created_at(self):
        return self._get_property('createdAt')

    @property
    def tracking(self):
        return self._get_property('tracking')

    def has_tracking(self):
        return self.tracking is not None

    def has_tracking_url(self):
        return self.has_tracking() and self.tracking['url'] is not None

    @property
    def tracking_url(self):
        return self.tracking['url'] if self.has_tracking_url() else None

    @property
    def lines(self):
        """Return the order lines of this shipment."""
        lines = self._get_property('lines') or []
        result = {
            '_embedded': {
                'lines': lines,
            },
            'count': len(lines),
        }
        return List(result, OrderLine, client=self.client)

    @property
    def order(self):
        """Return the order of this shipment."""
        from .order import Order
        url = self._get_link('order')
        if url:
            resp = self._resource.perform_api_call(self._resource.REST_READ, url)
            return Order(resp)
