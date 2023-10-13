from typing import TYPE_CHECKING, Any, Dict, Optional

from ..objects.order import Order
from ..objects.shipment import Shipment
from .base import ResourceCreateMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin

if TYPE_CHECKING:
    from ..client import Client

__all__ = [
    "OrderShipments",
]


class OrderShipments(ResourceCreateMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin):
    """Resource handler for the `/orders/:order_id:/shipments` endpoint."""

    RESOURCE_ID_PREFIX: str = "shp_"
    object_type = Shipment

    _order: Order

    def __init__(self, client: "Client", order: Order) -> None:
        self._order = order
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"orders/{self._order.id}/shipments"

    def create(self, data: Optional[Dict[str, Any]] = None, idempotency_key: str = "", **params: Any) -> Shipment:
        """Create a shipment for an order.

        If the data parameter is omitted, a shipment for all order lines is assumed.
        """
        if data is None:
            data = {"lines": []}
        return super().create(data, idempotency_key, **params)

    def get(self, resource_id: str, **params: Any) -> Shipment:
        self.validate_resource_id(resource_id, "shipment ID")
        return super().get(resource_id, **params)

    def update(
        self, resource_id: str, data: Optional[Dict[str, Any]] = None, idempotency_key: str = "", **params: Any
    ) -> Shipment:
        self.validate_resource_id(resource_id, "shipment ID")
        return super().update(resource_id, data, idempotency_key, **params)
