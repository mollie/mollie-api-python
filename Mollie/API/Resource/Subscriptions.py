from .Base import *
from Mollie.API.Error import *
from Mollie.API.Object import Subscription


class Subscriptions(Base):
    RESOURCE_ID_PREFIX = 'sub_'
    customer_id = None

    def getResourceObject(self, result):
        return Subscription(result)

    def get(self, subscription_id):
        if not subscription_id or not subscription_id.startswith(self.RESOURCE_ID_PREFIX):
            raise Error(
                'Invalid subscription ID: "%s". A subscription ID should start with "%s".' % (subscription_id, self.RESOURCE_ID_PREFIX)
            )
        return super(Subscriptions, self).get(subscription_id)

    def getResourceName(self):
        return 'customers/%s/subscriptions' % self.customer_id

    def withParentId(self, customer_id):
        self.customer_id = customer_id
        return self

    def on(self, customer):
        return self.withParentId(customer['id'])
