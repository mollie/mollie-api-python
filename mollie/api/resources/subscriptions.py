from typing import Optional

from ..objects.subscription import Subscription
from .base import ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin

__all__ = [
    "CustomerSubscriptions",
    "Subscriptions",
]


class SubscriptionsBase:
    RESOURCE_ID_PREFIX = "sub_"

    def get_resource_object(self, result: dict) -> Subscription:
        return Subscription(result, self.client)  # type: ignore


class Subscriptions(SubscriptionsBase, ResourceListMixin):
    """Resource handler for the `/subscriptions` endpoint."""

    pass


class CustomerSubscriptions(
    SubscriptionsBase,
    ResourceCreateMixin,
    ResourceDeleteMixin,
    ResourceGetMixin,
    ResourceListMixin,
    ResourceUpdateMixin,
):
    """Resource handler for the `/customers/:customer_id:/subscriptions` endpoint."""

    _customer = None

    def __init__(self, client, customer):
        self._customer = customer
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"customers/{self._customer.id}/subscriptions"  # type:ignore

    def get(self, resource_id: str, **params):
        self.validate_resource_id(resource_id, "subscription ID")
        return super().get(resource_id, **params)

    def update(self, resource_id: str, data: Optional[dict] = None, **params):
        self.validate_resource_id(resource_id, "subscription ID")
        return super().update(resource_id, data, **params)

    def delete(self, resource_id: str, **params):
        self.validate_resource_id(resource_id, "subscription ID")
        resp = super().delete(resource_id, **params)
        return self.get_resource_object(resp)
