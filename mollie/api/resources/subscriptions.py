from typing import TYPE_CHECKING, Any, Dict, Optional

from ..objects.customer import Customer
from ..objects.subscription import Subscription
from .base import (
    ResourceBase,
    ResourceCreateMixin,
    ResourceDeleteMixin,
    ResourceGetMixin,
    ResourceListMixin,
    ResourceUpdateMixin,
)

if TYPE_CHECKING:
    from ..client import Client

__all__ = [
    "CustomerSubscriptions",
    "Subscriptions",
]


class SubscriptionsBase(ResourceBase):
    RESOURCE_ID_PREFIX: str = "sub_"
    object_type = Subscription


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

    _customer: Customer

    def __init__(self, client: "Client", customer: Customer) -> None:
        self._customer = customer
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"customers/{self._customer.id}/subscriptions"

    def get(self, resource_id: str, **params: Any) -> Subscription:
        self.validate_resource_id(resource_id, "subscription ID")
        return super().get(resource_id, **params)

    def update(
        self, resource_id: str, data: Optional[Dict[str, Any]] = None, idempotency_key: str = "", **params: Any
    ) -> Subscription:
        self.validate_resource_id(resource_id, "subscription ID")
        return super().update(resource_id, data, idempotency_key, **params)

    def delete(self, resource_id: str, idempotency_key: str = "", **params: Any) -> dict:
        self.validate_resource_id(resource_id, "subscription ID")
        resp = super().delete(resource_id, idempotency_key, **params)
        return Subscription(resp, self.client)
