from Mollie.API.Resource import Payments


class CustomerPayments(Payments):
    customer_id = None

    def getResourceName(self):
        return 'customers/%s/payments' % self.customer_id

    def withParentId(self, customer_id):
        self.customer_id = customer_id
        return self

    def on(self, customer):
        return self.withParentId(customer['id'])
