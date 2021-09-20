from ..error import IdentifierError
from ..objects.mandate import Mandate
from .base import ResourceBase


class CustomerMandates(ResourceBase):
    RESOURCE_ID_PREFIX = "mdt_"
    customer_id = None

    def get_resource_object(self, result):
        return Mandate(result, self.client)

    def get(self, mandate_id, **params):
        if not mandate_id or not mandate_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                f"Invalid mandate ID: '{mandate_id}'. A mandate ID should start with '{self.RESOURCE_ID_PREFIX}'."
            )
        return super().get(mandate_id, **params)

    def get_resource_name(self):
        return f"customers/{self.customer_id}/mandates"

    def with_parent_id(self, customer_id):
        self.customer_id = customer_id
        return self

    def on(self, customer):
        return self.with_parent_id(customer.id)
