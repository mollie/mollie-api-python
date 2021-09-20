from ..error import IdentifierError
from ..objects.invoice import Invoice
from .base import ResourceBase


class Invoices(ResourceBase):
    RESOURCE_ID_PREFIX = "inv_"

    def get_resource_object(self, result):
        return Invoice(result, self.client)

    def get(self, invoice_id, **params):
        if not invoice_id or not invoice_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                f"Invalid invoice ID: '{invoice_id}'. An invoice ID should start with '{self.RESOURCE_ID_PREFIX}'."
            )
        return super().get(invoice_id, **params)
