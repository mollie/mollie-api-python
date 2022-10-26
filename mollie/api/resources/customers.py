from ..objects.customer import Customer
from .base import (
    ResourceBase,
    ResourceCreateMixin,
    ResourceDeleteMixin,
    ResourceGetMixin,
    ResourceListMixin,
    ResourceUpdateMixin,
)


class Customers(
    ResourceBase, ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin
):
    RESOURCE_ID_PREFIX = "cst_"

    def get_resource_object(self, result):
        return Customer(result, self.client)

    def get(self, customer_id: str, **params):
        self.validate_resource_id(customer_id, "customer ID")
        return super().get(customer_id, **params)

    def update(self, customer_id: str, data: dict, **params):
        self.validate_resource_id(customer_id, "customer ID")
        return super().update(customer_id, data, **params)

    def delete(self, customer_id: str, **params):
        self.validate_resource_id(customer_id, "customer ID")
        return super().delete(customer_id, **params)
