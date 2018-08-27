from .payments import Payments


class CustomerPayments(Payments):
    customer_id = None

    def get_resource_name(self):
        return 'customers/{id}/payments'.format(id=self.customer_id)

    def with_parent_id(self, customer_id):
        self.customer_id = customer_id
        return self

    def on(self, customer):
        return self.with_parent_id(customer.id)
