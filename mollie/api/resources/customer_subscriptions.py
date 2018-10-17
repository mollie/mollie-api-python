from ..error import IdentifierError
from ..objects.subscription import Subscription
from .base import Base


class CustomerSubscriptions(Base):
    RESOURCE_ID_PREFIX = 'sub_'
    customer_id = None

    def get_resource_object(self, result):
        return Subscription(result, self)

    def get(self, subscription_id, **params):
        if not subscription_id or not subscription_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                "Invalid subscription ID: '{id}'. A subscription ID should start with '{prefix}'.".format(
                    id=subscription_id, prefix=self.RESOURCE_ID_PREFIX)
            )
        return super(CustomerSubscriptions, self).get(subscription_id, **params)

    def delete(self, subscription_id, data=None):
        """Cancel subscription and return the subscription object.

        Deleting a subscription causes the subscription status to changed to 'canceled'.
        The updated subscription object is returned.
        """
        if not subscription_id or not subscription_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                "Invalid subscription ID: '{id}'. A subscription ID should start with '{prefix}'.".format(
                    id=subscription_id, prefix=self.RESOURCE_ID_PREFIX)
            )
        result = super(CustomerSubscriptions, self).delete(subscription_id, data)
        return self.get_resource_object(result)

    def get_resource_name(self):
        return 'customers/{id}/subscriptions'.format(id=self.customer_id)

    def with_parent_id(self, customer_id):
        self.customer_id = customer_id
        return self

    def on(self, customer):
        return self.with_parent_id(customer.id)
