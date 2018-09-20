from .base import Base
from .list import List
from .order_line import OrderLine
from .order import Order


class Shipment(Base):
    def __init__(self, data, resource=None, client=None):
        """
        Override the super __init__ to assign the Client to the result object, which is more flexible since it's
        not tied to a single API resource type
        """
        super(Shipment, self).__init__(data, resource)
        self.client = client

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

    @property
    def lines(self):
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
        url = self._get_link('order')
        if url:
            resp = self._resource.perform_api_call(self._resource.REST_READ, url)
            return Order(resp)

    def has_tracking(self):
        return self.tracking is not None

    def has_tracking_url(self):
        return self.has_tracking() and self.tracking['url'] is not None

    def tracking_url(self):
        return self._get_property('tracking', 'url')
