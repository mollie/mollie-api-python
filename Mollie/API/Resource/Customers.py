from .Base import Base
from Mollie.API.Error import Error
from Mollie.API.Object import Customer


class Customers(Base):
    RESOURCE_ID_PREFIX = 'cst_'

    def getResourceObject(self, result):
        return Customer(result)

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
