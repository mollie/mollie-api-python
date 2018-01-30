from .Base import Base
from Mollie.API.Error import Error
from Mollie.API.Object import Mandate


class CustomerMandates(Base):
    RESOURCE_ID_PREFIX = 'mdt_'
    customer_id = None

    def getResourceObject(self, result):
        return Mandate(result)

    def get(self, mandate_id, **params):
        if not mandate_id or not mandate_id.startswith(self.RESOURCE_ID_PREFIX):
            raise Error(
                'Invalid mandate ID: "%s". A mandate ID should start with "%s".' % (mandate_id, self.RESOURCE_ID_PREFIX)
            )
        return super(CustomerMandates, self).get(mandate_id)

    def getResourceName(self):
        return 'customers/%s/mandates' % self.customer_id

    def withParentId(self, customer_id):
        self.customer_id = customer_id
        return self

    def on(self, customer):
        return self.withParentId(customer['id'])
