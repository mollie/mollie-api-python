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
    RESOURCE_ID_PREFIX = "sub_"

    def get_resource_object(self, result):
        return Subscription(result, self.client)


class Subscriptions(SubscriptionsBase, ResourceListMixin):
    pass


class CustomerSubscriptions(
    SubscriptionsBase,
    ResourceCreateMixin,
    ResourceDeleteMixin,
    ResourceGetMixin,
    ResourceListMixin,
    ResourceUpdateMixin,
):
    _customer = None

    def __init__(self, client, customer):
        self._customer = customer
        super().__init__(client)

    def get_resource_path(self):
        return f"customers/{self._customer.id}/subscriptions"

    def get(self, subscription_id: str, **params):
        self.validate_resource_id(subscription_id, "subscription ID")
        return super().get(subscription_id, **params)

    def update(self, subscription_id: str, data: dict, **params):
        self.validate_resource_id(subscription_id, "subscription ID")
        return super().update(subscription_id, data, **params)

    def delete(self, subscription_id: str, **params):
        self.validate_resource_id(subscription_id, "subscription ID")
        resp = super().delete(subscription_id, **params)
        return self.get_resource_object(resp)
