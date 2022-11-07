from ..objects.invoice import Invoice
from .base import ResourceGetMixin, ResourceListMixin

__all__ = [
    "Invoices",
]


class Invoices(ResourceGetMixin, ResourceListMixin):
    """Resource handler for the `/invoices` endpoint."""

    RESOURCE_ID_PREFIX = "inv_"

    def get_resource_object(self, result: dict) -> Invoice:
        return Invoice(result, self.client)

    def get(self, resource_id: str, **params):
        self.validate_resource_id(resource_id, "invoice ID")
        return super().get(resource_id, **params)
