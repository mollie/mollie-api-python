from typing import Optional

from ..objects.customer import Customer
from .base import ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin


class Customers(ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin):
    """Resource handler for the `/customers` endpoint."""

    RESOURCE_ID_PREFIX = "cst_"

    def get_resource_object(self, result: dict) -> Customer:
        return Customer(result, self.client)

    def get(self, resource_id: str, **params):
        self.validate_resource_id(resource_id, "customer ID")
        return super().get(resource_id, **params)

    def update(self, resource_id: str, data: Optional[dict] = None, **params):
        self.validate_resource_id(resource_id, "customer ID")
        return super().update(resource_id, data, **params)

    def delete(self, resource_id: str, **params):
        self.validate_resource_id(resource_id, "customer ID")
        return super().delete(resource_id, **params)
