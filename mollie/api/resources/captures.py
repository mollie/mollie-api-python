from typing import Any

from ..objects.capture import Capture
from .base import ResourceBase, ResourceGetMixin, ResourceListMixin

__all__ = [
    "PaymentCaptures",
    "SettlementCaptures",
]


class CapturesBase(ResourceBase):
    RESOURCE_ID_PREFIX: str = "cpt_"

    def get_resource_object(self, result: dict) -> Capture:
        return Capture(result, self.client)


class PaymentCaptures(CapturesBase, ResourceGetMixin, ResourceListMixin):
    """Resource handler for the `/payments/:payment_id:/captures` endpoint."""

    def get(self, resource_id: str, **params: Any) -> Capture:
        self.validate_resource_id(resource_id, "capture ID")
        return super().get(resource_id, **params)


class SettlementCaptures(CapturesBase, ResourceListMixin):
    """Resource handler for the `/settlements/:settlement_id:/captures` endpoint."""

    pass
