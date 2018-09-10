from ..error import IdentifierError
from ..objects.mandate import Mandate
from .base import Base


class CustomerMandates(Base):
    RESOURCE_ID_PREFIX = 'mdt_'
    customer_id = None

    def get_resource_object(self, result):
        return Mandate(result, self)

    def get(self, mandate_id, **params):
        if not mandate_id or not mandate_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                "Invalid mandate ID: '{id}'. A mandate ID should start with '{prefix}'.".format(
                    id=mandate_id, prefix=self.RESOURCE_ID_PREFIX)
            )
        return super(CustomerMandates, self).get(mandate_id, **params)

    def get_resource_name(self):
        return 'customers/{id}/mandates'.format(id=self.customer_id)

    def with_parent_id(self, customer_id):
        self.customer_id = customer_id
        return self

    def on(self, customer):
        return self.with_parent_id(customer.id)
