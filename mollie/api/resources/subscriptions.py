from ..objects.subscription import Subscription
from .base import Base


class Subscriptions(Base):
    def get_resource_object(self, result):
        return Subscription(result, self.client)

    def create(self, data=None, **params):
        raise NotImplementedError('The endpoint "create" is not supported.')

    def get(self, resource_id, **params):
        raise NotImplementedError('The endpoint "get" is not supported.')

    def update(self, resource_id, data=None, **params):
        raise NotImplementedError('The endpoint "update" is not supported.')

    def delete(self, resource_id, data=None):
        raise NotImplementedError('The endpoint "delete" is not supported.')
