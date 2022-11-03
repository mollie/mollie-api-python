from ..objects.chargeback import Chargeback
from .base import ResourceBase, ResourceGetMixin, ResourceListMixin

__all__ = [
    "Chargebacks",
    "PaymentChargebacks",
    "ProfileChargebacks",
    "SettlementChargebacks",
]


class ChargebacksBase:
    RESOURCE_ID_PREFIX = "chb_"

    def get_resource_object(self, result: dict) -> Chargeback:
        return Chargeback(result, self.client)  # type: ignore


class Chargebacks(ChargebacksBase, ResourceListMixin):
    pass


class PaymentChargebacks(ChargebacksBase, ResourceGetMixin, ResourceListMixin):
    _payment = None

    def __init__(self, client, payment):
        self._payment = payment
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"payments/{self._payment.id}/chargebacks"  # type: ignore

    def get(self, resource_id: str, **params):
        self.validate_resource_id(resource_id, "chargeback ID")
        return super().get(resource_id, **params)


class SettlementChargebacks(ChargebacksBase, ResourceListMixin):
    _settlement = None

    def __init__(self, client, settlement):
        self._settlement = settlement
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"settlements/{self._settlement.id}/chargebacks"  # type: ignore


class ProfileChargebacks(ChargebacksBase, ResourceBase):
    _profile = None

    def __init__(self, client, profile):
        self._profile = profile
        super().__init__(client)

    def list(self, **params):
        # Set the profileId in the query params
        params.update({"profileId": self._profile.id})
        return Chargebacks(self.client).list(**params)
