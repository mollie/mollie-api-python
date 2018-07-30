from .base import Base
from mollie.api.error import IdentifierValidationError
from mollie.api.objects import Subscription


class CustomerSubscriptions(Base):
    RESOURCE_ID_PREFIX = 'sub_'
    customer_id = None

    def get_resource_object(self, result):
        subscription = Subscription(result)
        subscription._resource = self
        return subscription

    def get(self, subscription_id, **params):
        if not subscription_id or not subscription_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierValidationError(
                'Invalid subscription ID: "%s". A subscription ID should start with "%s".' % (
                    subscription_id, self.RESOURCE_ID_PREFIX)
            )
        return super(CustomerSubscriptions, self).get(subscription_id)

    def delete(self, subscription_id):
        """Cancel subscription and return the subscription object.

        Deleting a subscription causes the subscription status to changed to 'canceled'.
        The updated subscription object is returned.
        """
        if not subscription_id or not subscription_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierValidationError(
                'Invalid subscription ID: "%s". A subscription ID should start with "%s".' % (
                    subscription_id, self.RESOURCE_ID_PREFIX)
            )
        result = super(CustomerSubscriptions, self).delete(subscription_id)
        return self.get_resource_object(result)

    def get_resource_name(self):
        return 'customers/%s/subscriptions' % self.customer_id

    def with_parent_id(self, customer_id):
        self.customer_id = customer_id
        return self

    def on(self, customer):
        return self.with_parent_id(customer.id)
