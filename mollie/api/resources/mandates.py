from typing import TYPE_CHECKING, Any

from ..objects.customer import Customer
from ..objects.mandate import Mandate
from .base import ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin

if TYPE_CHECKING:
    from ..client import Client


__all__ = [
    "CustomerMandates",
]


class CustomerMandates(ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin):
    """Resource handler for the `/customers/:customer_id:/mandates` endpoint."""

    RESOURCE_ID_PREFIX = "mdt_"

    _customer: Customer
    object_type = Mandate

    def __init__(self, client: "Client", customer: Customer) -> None:
        self._customer = customer
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"customers/{self._customer.id}/mandates"

    def get(self, resource_id: str, **params: Any) -> Mandate:
        self.validate_resource_id(resource_id, "mandate ID")
        return super().get(resource_id, **params)

    def delete(self, resource_id: str, idempotency_key: str = "", **params: Any) -> dict:
        self.validate_resource_id(resource_id, "mandate ID")
        return super().delete(resource_id, idempotency_key, **params)
