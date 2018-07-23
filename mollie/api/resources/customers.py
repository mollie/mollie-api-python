from .base import Base
from mollie.api.error import Error
from mollie.api.objects import Customer


class Customers(Base):
    RESOURCE_ID_PREFIX = 'cst_'

    def get_resource_object(self, result):
        customer = Customer(result)
        customer._resource = self
        return customer

    def get(self, customer_id, **params):
        if not customer_id or not customer_id.startswith(self.RESOURCE_ID_PREFIX):
            raise Error(
                'Invalid customer ID: "%s". A customer ID should start with "%s".' % (customer_id, self.RESOURCE_ID_PREFIX)
            )
        return super(Customers, self).get(customer_id)

    def mandates(self, customer):
        return self.client.customer_mandates.on(customer)

    def subscriptions(self, customer):
        return self.client.customer_subscriptions.on(customer)

    def payments(self, customer):
        return self.client.customer_payments.on(customer)
