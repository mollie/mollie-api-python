from ..objects.invoice import Invoice
from .base import ResourceBase, ResourceGetMixin, ResourceListMixin

__all__ = [
    "Invoices",
]


class Invoices(ResourceBase, ResourceGetMixin, ResourceListMixin):
    RESOURCE_ID_PREFIX = "inv_"

    def get_resource_object(self, result):
        return Invoice(result, self.client)

    def get(self, invoice_id: str, **params):
        self.validate_resource_id(invoice_id, "invoice ID")
        return super().get(invoice_id, **params)
