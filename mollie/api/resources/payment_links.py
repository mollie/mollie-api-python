from ..error import IdentifierError
from ..objects.payment_link import PaymentLink
from .base import ResourceBase


class PaymentLinks(ResourceBase):
    RESOURCE_ID_PREFIX = "pl_"

    def get_resource_object(self, result):
        return PaymentLink(result, self.client)

    def get_resource_name(self):
        return "payment-links"

    def get(self, payment_link_id, **params):
        if not payment_link_id or not payment_link_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                f"Invalid payment ID: '{payment_link_id}'. A payment ID should start with '{self.RESOURCE_ID_PREFIX}'."
            )
        return super().get(payment_link_id, **params)
