from ..error import IdentifierError
from ..objects.customer import Customer
from .base import ResourceBase


class Customers(ResourceBase):
    RESOURCE_ID_PREFIX = "cst_"

    def get_resource_object(self, result):
        return Customer(result, self.client)

    def get(self, customer_id, **params):
        if not customer_id or not customer_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                f"Invalid customer ID: '{customer_id}'. A customer ID should start with '{self.RESOURCE_ID_PREFIX}'."
            )
        return super().get(customer_id, **params)
