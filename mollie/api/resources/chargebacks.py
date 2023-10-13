from typing import TYPE_CHECKING, Any

from ..objects.chargeback import Chargeback
from ..objects.list import PaginationList
from .base import ResourceBase, ResourceGetMixin, ResourceListMixin

if TYPE_CHECKING:
    from ..client import Client
    from ..objects.payment import Payment
    from ..objects.profile import Profile
    from ..objects.settlement import Settlement

__all__ = [
    "Chargebacks",
    "PaymentChargebacks",
    "ProfileChargebacks",
    "SettlementChargebacks",
]


class ChargebacksBase(ResourceBase):
    RESOURCE_ID_PREFIX: str = "chb_"
    object_type = Chargeback


class Chargebacks(ChargebacksBase, ResourceListMixin):
    """Resource handler for the `/chargebacks` endpoint."""

    pass


class PaymentChargebacks(ChargebacksBase, ResourceGetMixin, ResourceListMixin):
    """Resource handler for the `/payments/:payment_id:/chargebacks` endpoint."""

    _payment: "Payment"

    def __init__(self, client: "Client", payment: "Payment") -> None:
        self._payment = payment
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"payments/{self._payment.id}/chargebacks"

    def get(self, resource_id: str, **params: Any) -> Chargeback:
        self.validate_resource_id(resource_id, "chargeback ID")
        return super().get(resource_id, **params)


class SettlementChargebacks(ChargebacksBase, ResourceListMixin):
    """Resource handler for the `/settlements/:settlement_id:/chargebacks` endpoint."""

    _settlement: "Settlement"

    def __init__(self, client: "Client", settlement: "Settlement") -> None:
        self._settlement = settlement
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"settlements/{self._settlement.id}/chargebacks"


class ProfileChargebacks(ChargebacksBase):
    """
    Resource handler for the `/chargebacks?profileId=:profile_id:` endpoint.

    This is separate from the `Chargebacks` resource handler to make it easier to inject the profileId.
    """

    _profile: "Profile"

    def __init__(self, client: "Client", profile: "Profile") -> None:
        self._profile = profile
        super().__init__(client)

    def list(self, **params: Any) -> PaginationList:
        # Set the profileId in the query params
        params.update({"profileId": self._profile.id})
        return Chargebacks(self.client).list(**params)
