from ..objects.shipment import Shipment
from .base import ResourceBase, ResourceCreateMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin

__all__ = [
    "OrderShipments",
]


class OrderShipments(ResourceBase, ResourceCreateMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin):
    RESOURCE_ID_PREFIX = "shp_"

    _order = None

    def __init__(self, client, order):
        self._order = order
        super().__init__(client)

    def get_resource_object(self, result):
        return Shipment(result, self.client)

    def get_resource_path(self):
        return f"orders/{self._order.id}/shipments"

    def create(self, data=None, **params):
        """Create a shipment for an order.

        If the data parameter is omitted, a shipment for all order lines is assumed.
        """
        if data is None:
            data = {"lines": []}
        return super().create(data, **params)

    def get(self, shipment_id, **params):
        self.validate_resource_id(shipment_id, "shipment ID")
        return super().get(shipment_id, **params)

    def update(self, shipment_id, data, **params):
        self.validate_resource_id(shipment_id, "shipment ID")
        return super().update(shipment_id, data, **params)
