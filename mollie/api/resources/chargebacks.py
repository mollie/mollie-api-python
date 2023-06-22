from typing import Any

from ..objects.chargeback import Chargeback
from .base import ResourceBase, ResourceGetMixin, ResourceListMixin

__all__ = [
    "Chargebacks",
    "PaymentChargebacks",
    "ProfileChargebacks",
    "SettlementChargebacks",
]


class ChargebacksBase(ResourceBase):
    RESOURCE_ID_PREFIX: str = "chb_"

    def get_resource_object(self, result: dict) -> Chargeback:
        return Chargeback(result, self.client)


class Chargebacks(ChargebacksBase, ResourceListMixin):
    """Resource handler for the `/chargebacks` endpoint."""

    pass


class PaymentChargebacks(ChargebacksBase, ResourceGetMixin, ResourceListMixin):
    """Resource handler for the `/payments/:payment_id:/chargebacks` endpoint."""

    def get(self, resource_id: str, **params: Any) -> Chargeback:
        self.validate_resource_id(resource_id, "chargeback ID")
        return super().get(resource_id, **params)


class SettlementChargebacks(ChargebacksBase, ResourceListMixin):
    """Resource handler for the `/settlements/:settlement_id:/chargebacks` endpoint."""

    pass


class ProfileChargebacks(Chargebacks):
    """
    Resource handler for the `/chargebacks?profileId=:profile_id:` endpoint.

    This is completely equal to Chargebacks, just here for completeness.
    """

    pass
