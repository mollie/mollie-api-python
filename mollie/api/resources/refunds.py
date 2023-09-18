from typing import TYPE_CHECKING, Any, Dict, Optional

from ..objects.list import PaginationList
from ..objects.order import Order
from ..objects.payment import Payment
from ..objects.profile import Profile
from ..objects.refund import Refund
from .base import ResourceBase, ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin

if TYPE_CHECKING:
    from ..client import Client
    from ..objects.settlement import Settlement

__all__ = [
    "OrderRefunds",
    "PaymentRefunds",
    "ProfileRefunds",
    "Refunds",
    "SettlementRefunds",
]


class RefundsBase(ResourceBase):
    RESOURCE_ID_PREFIX: str = "re_"
    object_type = Refund


class Refunds(RefundsBase, ResourceListMixin):
    """Resource handler for the `/refunds` endpoint."""

    pass


class PaymentRefunds(RefundsBase, ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin):
    """Resource handler for the `/payments/:payment_id:/refunds` endpoint."""

    _payment: Payment

    def __init__(self, client: "Client", payment: Payment) -> None:
        self._payment = payment
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"payments/{self._payment.id}/refunds"

    def get(self, resource_id: str, **params: Any) -> Refund:
        self.validate_resource_id(resource_id, "Refund ID")
        return super().get(resource_id, **params)

    def delete(self, resource_id: str, idempotency_key: str = "", **params: Any) -> dict:
        self.validate_resource_id(resource_id, "Refund ID")
        return super().delete(resource_id, idempotency_key, **params)


class OrderRefunds(RefundsBase, ResourceCreateMixin, ResourceListMixin):
    """Resource handler for the `/orders/:order_id:/refunds` endpoint."""

    _order: Order

    def __init__(self, client: "Client", order: Order) -> None:
        super().__init__(client)
        self._order = order

    def get_resource_path(self) -> str:
        return f"orders/{self._order.id}/refunds"

    def create(self, data: Optional[Dict[str, Any]] = None, idempotency_key: str = "", **params: Any) -> Refund:
        """Create a refund for the order. When no data arg is given, a refund for all order lines is assumed."""
        if not data:
            data = {"lines": []}
        return super().create(data, idempotency_key, **params)


class SettlementRefunds(RefundsBase, ResourceListMixin):
    """ResourceHandler for the `/settlements/:settlement_id:/refunds` endpoint."""

    _settlement: "Settlement"

    def __init__(self, client: "Client", settlement: "Settlement"):
        super().__init__(client)
        self._settlement = settlement

    def get_resource_path(self) -> str:
        return f"settlements/{self._settlement.id}/refunds"


class ProfileRefunds(RefundsBase):
    """
    Resource handler for the `/refunds?profileId=:profile_id:` endpoint.

    This is separate from the `Refunds` resource handler to make it easier to inject the profileId.
    """

    _profile: Profile

    def __init__(self, client: "Client", profile: Profile) -> None:
        self._profile = profile
        super().__init__(client)

    def list(self, **params: Any) -> PaginationList:
        # Set the profileId in the query params
        params.update({"profileId": self._profile.id})
        return Refunds(self.client).list(**params)
