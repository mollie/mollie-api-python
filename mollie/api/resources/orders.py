from typing import Optional

from ..objects.order import Order
from .base import ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin

__all__ = [
    "Orders",
]


class Orders(ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin):
    """Resource handler for the `/orders` endpoint."""

    RESOURCE_ID_PREFIX = "ord_"

    def get_resource_object(self, result: dict) -> Order:
        return Order(result, self.client)

    def get(self, resource_id: str, **params):
        self.validate_resource_id(resource_id, "order ID")
        return super().get(resource_id, **params)

    def delete(self, resource_id: str, **params):
        """Cancel order and return the order object.

        Deleting an order causes the order status to change to canceled.
        The updated order object is returned.
        """
        self.validate_resource_id(resource_id, "order ID")
        result = super().delete(resource_id, **params)
        return self.get_resource_object(result)

    def update(self, resource_id: str, data: Optional[dict] = None, **params):
        """Update an order, and return the updated order."""
        self.validate_resource_id(resource_id, "order ID")
        return super().update(resource_id, data, **params)
