from typing import Any

from ..objects.mandate import Mandate
from .base import ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin

__all__ = [
    "CustomerMandates",
]


class CustomerMandates(ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin):
    """Resource handler for the `/customers/:customer_id:/mandates` endpoint."""

    RESOURCE_ID_PREFIX = "mdt_"

    def get_resource_object(self, result: dict) -> Mandate:
        return Mandate(result, self.client)

    def get(self, resource_id: str, **params: Any) -> Mandate:
        self.validate_resource_id(resource_id, "mandate ID")
        return super().get(resource_id, **params)

    def delete(self, resource_id: str, idempotency_key: str = "", **params: Any) -> dict:
        self.validate_resource_id(resource_id, "mandate ID")
        return super().delete(resource_id, idempotency_key, **params)
