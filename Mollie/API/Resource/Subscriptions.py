from .Base import *
from Mollie.API.Object import Subscription


class Subscriptions(Base):
    customer_id = None

    def getResourceObject(self, result):
        return Subscription(result)

    def getResourceName(self):
        return 'customers/%s/subscriptions' % self.customer_id

    def on(self, customer):
        self.customer_id = customer['id']
        return self
