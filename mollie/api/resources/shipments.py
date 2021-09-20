from ..objects.shipment import Shipment
from .base import ResourceBase


class Shipments(ResourceBase):
    order_id = None

    def get_resource_object(self, result):
        return Shipment(result, self.client)

    def get_resource_name(self):
        return f"orders/{self.order_id}/shipments"

    def with_parent_id(self, order_id):
        self.order_id = order_id
        return self

    def on(self, order):
        return self.with_parent_id(order.id)
