from ..error import IdentifierError
from ..objects.invoice import Invoice
from .base import Base


class Invoices(Base):
    RESOURCE_ID_PREFIX = 'inv_'

    def get_resource_object(self, result):
        return Invoice(result, self.client)

    def get(self, invoice_id, **params):
        if not invoice_id or not invoice_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                "Invalid invoice ID: '{id}'. A invoice ID should start with '{prefix}'.".format(
                    id=invoice_id, prefix=self.RESOURCE_ID_PREFIX)
            )
        return super().get(invoice_id, **params)
