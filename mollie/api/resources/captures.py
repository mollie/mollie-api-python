from ..objects.capture import Capture
from .base import ResourceGetMixin, ResourceListMixin

__all__ = [
    "PaymentCaptures",
    "SettlementCaptures",
]


class CapturesBase:
    RESOURCE_ID_PREFIX = "cpt_"

    def get_resource_object(self, result: dict) -> Capture:
        return Capture(result, self.client)  # type: ignore


class PaymentCaptures(CapturesBase, ResourceGetMixin, ResourceListMixin):
    """Resource handler for the `/payments/:payment_id:/captures` endpoint."""

    _payment = None

    def __init__(self, client, payment):
        self._payment = payment
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"payments/{self._payment.id}/captures"  # type:ignore

    def get(self, resource_id: str, **params):
        self.validate_resource_id(resource_id, "capture ID")
        return super().get(resource_id, **params)


class SettlementCaptures(CapturesBase, ResourceListMixin):
    """Resource handler for the `/settlements/:settlement_id:/captures` endpoint."""

    _settlement = None

    def __init__(self, client, settlement):
        self._settlement = settlement
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"settlements/{self._settlement.id}/captures"  # type:ignore
