from ..error import IdentifierError
from ..objects.customer import Customer
from .base import Base


class Customers(Base):
    RESOURCE_ID_PREFIX = 'cst_'

    def get_resource_object(self, result):
        customer = Customer(result)
        customer._resource = self
        return customer

    def get(self, customer_id, **params):
        if not customer_id or not customer_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                'Invalid customer ID: "%s". A customer ID should start with "%s".' % (
                    customer_id, self.RESOURCE_ID_PREFIX)
            )
        return super(Customers, self).get(customer_id)
