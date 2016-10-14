from .Base import *
from Mollie.API.Object import Payment


class CustomerPayments(Base):
    customer_id = None

    def getResourceObject(self, result):
        return Payment(result)

    def getResourceName(self):
        return 'customers/%s/payments' % self.customer_id

    def withParentId(self, customer_id):
        self.customer_id = customer_id
        return self

    def on(self, customer):
        return self.withParentId(customer['id'])
