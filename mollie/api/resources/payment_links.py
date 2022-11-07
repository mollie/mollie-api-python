from ..objects.payment_link import PaymentLink
from .base import ResourceCreateMixin, ResourceGetMixin, ResourceListMixin

__all__ = [
    "PaymentLinks",
]


class PaymentLinks(ResourceCreateMixin, ResourceGetMixin, ResourceListMixin):
    """Resource handler for the `/payment_links` endpoint."""

    RESOURCE_ID_PREFIX = "pl_"

    def get_resource_path(self) -> str:
        return "payment-links"

    def get_resource_object(self, result) -> PaymentLink:
        return PaymentLink(result, self.client)  # type: ignore

    def get(self, resource_id: str, **params):
        self.validate_resource_id(resource_id, "payment link ID")
        return super().get(resource_id, **params)
