from ..objects.subscription import Subscription
from .base import ResourceBase, ResourceListMixin


class Subscriptions(ResourceBase, ResourceListMixin):
    def get_resource_object(self, result):
        return Subscription(result, self.client)
