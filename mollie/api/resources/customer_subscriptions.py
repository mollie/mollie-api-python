from .base import Base
from mollie.api.error import Error
from mollie.api.objects import Subscription


class CustomerSubscriptions(Base):
    RESOURCE_ID_PREFIX = 'sub_'
    customer_id = None

    def get_resource_object(self, result):
        return Subscription(result)

    def get(self, subscription_id, **params):
        if not subscription_id or not subscription_id.startswith(self.RESOURCE_ID_PREFIX):
            raise Error(
                'Invalid subscription ID: "%s". A subscription ID should start with "%s".' % (subscription_id, self.RESOURCE_ID_PREFIX)
            )
        return super(CustomerSubscriptions, self).get(subscription_id)

    def get_resource_name(self):
        return 'customers/%s/subscriptions' % self.customer_id

    def with_parent_id(self, customer_id):
        self.customer_id = customer_id
        return self

    def on(self, customer):
        return self.with_parent_id(customer['id'])
