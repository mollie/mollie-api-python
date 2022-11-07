from ..objects.mandate import Mandate
from .base import ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin

__all__ = [
    "CustomerMandates",
]


class CustomerMandates(ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin):
    """Resource handler for the `/customers/:customer_id:/mandates` endpoint."""

    RESOURCE_ID_PREFIX = "mdt_"

    _customer = None

    def __init__(self, client, customer):
        self._customer = customer
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"customers/{self._customer.id}/mandates"  # type: ignore

    def get_resource_object(self, result: dict) -> Mandate:
        return Mandate(result, self.client)

    def get(self, resource_id: str, **params):
        self.validate_resource_id(resource_id, "mandate ID")
        return super().get(resource_id, **params)

    def delete(self, resource_id: str, **params):
        self.validate_resource_id(resource_id, "mandate ID")
        return super().delete(resource_id, **params)
