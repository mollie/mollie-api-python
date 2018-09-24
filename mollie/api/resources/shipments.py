from ..objects.shipment import Shipment
from .base import Base


class Shipments(Base):
    order_id = None

    def get_resource_object(self, result):
        return Shipment(result, client=self.client)

    def get_resource_name(self):
        return 'orders/{id}/shipments'.format(id=self.order_id)

    def with_parent_id(self, order_id):
        self.order_id = order_id
        return self

    def on(self, order):
        return self.with_parent_id(order.id)
