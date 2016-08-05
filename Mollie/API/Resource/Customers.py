from Mollie.API import Payments
from Mollie.API.Resource.Base import *
from Mollie.API.Error import *


class Customers(Base):
    RESOURCE_ID_PREFIX = 'cst_'

    def getResourceObject(self, result):
        return Customer(result)

    def get(self, customer_id):
        if not customer_id or self.RESOURCE_ID_PREFIX not in customer_id:
            raise Error(
                'Invalid customer ID: "%s". A customer ID should start with '
                '"%s".' % (
                    customer_id, self.RESOURCE_ID_PREFIX)
            )
        return super(Customers, self).get(customer_id)


class CustomerPayments(Base):
    RESOURCE_ID_PREFIX = 'tr_'

    customer_id = None

    def withParentId(self, customer_id=None):
        self.customer_id = customer_id

    def getResourceObject(self, result):
        return Payment(result)

    def getResourceName(self):
        return '{}/{}/{}'.format(Customers.__class__.__name__.lower(),
                                 self.customer_id,
                                 Payments.__class__.__name__.lower())

    def create(self, data):
        if self.customer_id is None:
            raise Error('Invalid customer ID')
        return super(CustomerPayments, self).create(data)

    def get(self, resource_id):
        if self.customer_id is None:
            raise Error('Invalid customer ID')
        if not resource_id or self.RESOURCE_ID_PREFIX not in resource_id:
            raise Error(
                'Invalid payment ID: "%s". A payment ID should start with '
                '"%s".' % (
                    resource_id, self.RESOURCE_ID_PREFIX)
            )
        return super(CustomerPayments, self).get(resource_id)

    def update(self, resource_id, data):
        if self.customer_id is None:
            raise Error('Invalid customer ID')
        return super(CustomerPayments, self).update(resource_id, data)

    def delete(self, resource_id):
        if self.customer_id is None:
            raise Error('Invalid customer ID')
        return super(CustomerPayments, self).delete(resource_id)

    def all(self, offset=0, count=Base.DEFAULT_LIMIT):
        if self.customer_id is None:
            raise Error('Invalid customer ID')
        return super(CustomerPayments, self).all(offset, count)
