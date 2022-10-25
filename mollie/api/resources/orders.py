from ..objects.order import Order
from .base import (
    ResourceBase,
    ResourceCreateMixin,
    ResourceDeleteMixin,
    ResourceGetMixin,
    ResourceListMixin,
    ResourceUpdateMixin,
)

__all__ = [
    "Orders",
]


class Orders(
    ResourceBase, ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin
):
    RESOURCE_ID_PREFIX = "ord_"

    def get_resource_object(self, result):
        return Order(result, self.client)

    def get(self, order_id: str, **params):
        self.validate_resource_id(order_id, "order ID")
        order = super().get(order_id, **params)

        requested_embeds = self.extract_embed(params)
        if requested_embeds:
            order.requested_embeds = requested_embeds

        return order

    def delete(self, order_id: str, data=None):
        """Cancel order and return the order object.

        Deleting an order causes the order status to change to canceled.
        The updated order object is returned.
        """
        self.validate_resource_id(order_id, "order ID")
        result = super().delete(order_id, data)
        return self.get_resource_object(result)

    def update(self, order_id: str, data=None):
        """Update an order, and return the updated order."""
        self.validate_resource_id(order_id, "order ID")
        return super().update(order_id, data)
