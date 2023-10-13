from typing import Any

from ..objects.invoice import Invoice
from .base import ResourceGetMixin, ResourceListMixin

__all__ = [
    "Invoices",
]


class Invoices(ResourceGetMixin, ResourceListMixin):
    """Resource handler for the `/invoices` endpoint."""

    RESOURCE_ID_PREFIX: str = "inv_"
    object_type = Invoice

    def get(self, resource_id: str, **params: Any) -> Invoice:
        self.validate_resource_id(resource_id, "invoice ID")
        return super().get(resource_id, **params)
