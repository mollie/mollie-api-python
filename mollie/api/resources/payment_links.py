from ..objects.payment_link import PaymentLink
from .base import ResourceBase, ResourceCreateMixin, ResourceGetMixin, ResourceListMixin

__all__ = [
    "PaymentLinks",
]


class PaymentLinks(ResourceBase, ResourceCreateMixin, ResourceGetMixin, ResourceListMixin):
    RESOURCE_ID_PREFIX = "pl_"

    def get_resource_path(self):
        return "payment-links"

    def get_resource_object(self, result):
        return PaymentLink(result, self.client)

    def get(self, payment_link_id: str, **params):
        self.validate_resource_id(payment_link_id, "payment link ID")
        return super().get(payment_link_id, **params)
