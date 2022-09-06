from ..error import IdentifierError
from ..objects.subscription import Subscription
from .base import ResourceAllMethodsMixin, ResourceBase
from .customers import Customers


class Subscriptions(ResourceBase, ResourceAllMethodsMixin):
    RESOURCE_ID_PREFIX = "sub_"
    parent_id = None

    def get_resource_name(self):
        if not self.parent_id:
            return "subscriptions"

        if self.parent_id.startswith(Customers.RESOURCE_ID_PREFIX):
            return f"customers/{self.parent_id}/subscriptions"

        else:
            raise IdentifierError("Invalid Parent, the parent of a Capture should be a Payment or a Settlement.")

    def get_resource_object(self, result):
        return Subscription(result, self.client)

    def get(self, subscription_id, **params):
        if not subscription_id or not subscription_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                f"Invalid subscription ID: '{subscription_id}'. A subscription ID "
                f"should start with '{self.RESOURCE_ID_PREFIX}'."
            )
        return super().get(subscription_id, **params)

    def delete(self, subscription_id, data=None):
        """Cancel subscription and return the subscription object.

        Deleting a subscription causes the subscription status to changed to 'canceled'.
        The updated subscription object is returned.
        """
        if not subscription_id or not subscription_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                f"Invalid subscription ID: '{subscription_id}'. A subscription ID "
                f"should start with '{self.RESOURCE_ID_PREFIX}'."
            )
        result = super().delete(subscription_id, data)
        return self.get_resource_object(result)

    def with_parent_id(self, parent_id):
        self.parent_id = parent_id
        return self

    def on(self, parent):
        return self.with_parent_id(parent.id)
