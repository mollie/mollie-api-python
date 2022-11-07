from typing import Optional

from ..objects.shipment import Shipment
from .base import ResourceCreateMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin

__all__ = [
    "OrderShipments",
]


class OrderShipments(ResourceCreateMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin):
    """Resource handler for the `/orders/:order_id:/shipments` endpoint."""

    RESOURCE_ID_PREFIX = "shp_"

    _order = None

    def __init__(self, client, order):
        self._order = order
        super().__init__(client)

    def get_resource_object(self, result: dict) -> Shipment:
        return Shipment(result, self.client)  # type: ignore

    def get_resource_path(self) -> str:
        return f"orders/{self._order.id}/shipments"  # type: ignore

    def create(self, data: Optional[dict] = None, **params):
        """Create a shipment for an order.

        If the data parameter is omitted, a shipment for all order lines is assumed.
        """
        if data is None:
            data = {"lines": []}
        return super().create(data, **params)

    def get(self, resource_id: str, **params):
        self.validate_resource_id(resource_id, "shipment ID")
        return super().get(resource_id, **params)

    def update(self, resource_id: str, data: Optional[dict] = None, **params):
        self.validate_resource_id(resource_id, "shipment ID")
        return super().update(resource_id, data, **params)
