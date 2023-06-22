from typing import Any, Dict, Optional

from ..objects.subscription import Subscription
from .base import (
    ResourceBase,
    ResourceCreateMixin,
    ResourceDeleteMixin,
    ResourceGetMixin,
    ResourceListMixin,
    ResourceUpdateMixin,
)

__all__ = [
    "CustomerSubscriptions",
    "Subscriptions",
]


class SubscriptionsBase(ResourceBase):
    RESOURCE_ID_PREFIX: str = "sub_"

    def get_resource_object(self, result: dict) -> Subscription:
        return Subscription(result, self.client)


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
        return self.get_resource_object(resp)
