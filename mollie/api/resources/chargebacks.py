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
    """Resource handler for the `/chargebacks` endpoint."""

    pass


class PaymentChargebacks(ChargebacksBase, ResourceGetMixin, ResourceListMixin):
    """Resource handler for the `/payments/:payment_id:/chargebacks` endpoint."""

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
    """Resource handler for the `/settlements/:settlement_id:/chargebacks` endpoint."""

    _settlement = None

    def __init__(self, client, settlement):
        self._settlement = settlement
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"settlements/{self._settlement.id}/chargebacks"  # type: ignore


class ProfileChargebacks(ChargebacksBase, ResourceBase):
    """
    Resource handler for the `/chargebacks?profileId=:profile_id:` endpoint.

    This is separate from the `Chargebacks` resource handler to make it easier to inject the profileId.
    """

    _profile = None

    def __init__(self, client, profile):
        self._profile = profile
        super().__init__(client)

    def list(self, **params):
        # Set the profileId in the query params
        params.update({"profileId": self._profile.id})
        return Chargebacks(self.client).list(**params)
