from typing import TYPE_CHECKING, Any

from ..objects.capture import Capture
from .base import ResourceBase, ResourceCreateMixin, ResourceGetMixin, ResourceListMixin

if TYPE_CHECKING:
    from ..client import Client
    from ..objects.payment import Payment
    from ..objects.settlement import Settlement

__all__ = [
    "PaymentCaptures",
    "SettlementCaptures",
]


class CapturesBase(ResourceBase):
    RESOURCE_ID_PREFIX: str = "cpt_"
    object_type = Capture


class PaymentCaptures(CapturesBase, ResourceGetMixin, ResourceListMixin, ResourceCreateMixin):
    """Resource handler for the `/payments/:payment_id:/captures` endpoint."""

    _payment: "Payment"

    def __init__(self, client: "Client", payment: "Payment") -> None:
        self._payment = payment
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"payments/{self._payment.id}/captures"

    def get(self, resource_id: str, **params: Any) -> Capture:
        self.validate_resource_id(resource_id, "capture ID")
        return super().get(resource_id, **params)


class SettlementCaptures(CapturesBase, ResourceListMixin):
    """Resource handler for the `/settlements/:settlement_id:/captures` endpoint."""

    _settlement: "Settlement"

    def __init__(self, client: "Client", settlement: "Settlement") -> None:
        self._settlement = settlement
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"settlements/{self._settlement.id}/captures"
