from ..objects.capture import Capture
from .base import ResourceBase, ResourceGetMixin, ResourceListMixin


class CapturesBase(ResourceBase):
    RESOURCE_ID_PREFIX = "cpt_"

    def get_resource_object(self, result):
        return Capture(result, self.client)


class PaymentCaptures(CapturesBase, ResourceGetMixin, ResourceListMixin):
    _payment = None

    def __init__(self, client, payment):
        self._payment = payment
        super().__init__(client)

    def get_resource_path(self):
        return f"payments/{self._payment.id}/captures"

    def get(self, capture_id: str, **params):
        self.validate_resource_id(capture_id, "capture ID")
        return super().get(capture_id, **params)


class SettlementCaptures(CapturesBase, ResourceListMixin):
    _settlement = None

    def __init__(self, client, settlement):
        self._settlement = settlement
        super().__init__(client)

    def get_resource_path(self):
        return f"settlements/{self._settlement.id}/captures"
