from typing import Any, Dict, Optional

from ..objects.order import Order
from .base import ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin

__all__ = [
    "Orders",
]


class Orders(ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin):
    """Resource handler for the `/orders` endpoint."""

    RESOURCE_ID_PREFIX: str = "ord_"
    object_type = Order

    def get(self, resource_id: str, **params: Any) -> Order:
        self.validate_resource_id(resource_id, "order ID")
        return super().get(resource_id, **params)

    def delete(self, resource_id: str, idempotency_key: str = "", **params: Any) -> dict:
        """Cancel order and return the order object.

        Deleting an order causes the order status to change to canceled.
        The updated order object is returned.
        """
        self.validate_resource_id(resource_id, "order ID")
        result = super().delete(resource_id, **params)
        return Order(result, self.client)

    def update(
        self, resource_id: str, data: Optional[Dict[str, Any]] = None, idempotency_key: str = "", **params: Any
    ) -> Order:
        """Update an order, and return the updated order."""
        self.validate_resource_id(resource_id, "order ID")
        return super().update(resource_id, data, idempotency_key, **params)
