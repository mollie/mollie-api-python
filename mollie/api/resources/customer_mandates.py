from .base import Base

from mollie.api.error import IdentifierValidationError
from mollie.api.objects.mandate import Mandate


class CustomerMandates(Base):
    RESOURCE_ID_PREFIX = 'mdt_'
    customer_id = None

    def get_resource_object(self, result):
        mandate = Mandate(result)
        mandate._resource = self
        return mandate

    def get(self, mandate_id, **params):
        if not mandate_id or not mandate_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierValidationError(
                'Invalid mandate ID: "%s". A mandate ID should start with "%s".' % (
                    mandate_id, self.RESOURCE_ID_PREFIX)
            )
        return super(CustomerMandates, self).get(mandate_id)

    def get_resource_name(self):
        return 'customers/%s/mandates' % self.customer_id

    def with_parent_id(self, customer_id):
        self.customer_id = customer_id
        return self

    def on(self, customer):
        return self.with_parent_id(customer.id)
