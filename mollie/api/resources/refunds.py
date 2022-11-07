from typing import Optional

from ..objects.refund import Refund
from .base import ResourceBase, ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin

__all__ = [
    "OrderRefunds",
    "PaymentRefunds",
    "ProfileRefunds",
    "Refunds",
    "SettlementRefunds",
]


class RefundsBase:
    RESOURCE_ID_PREFIX = "re_"

    def get_resource_object(self, result: dict) -> Refund:
        return Refund(result, self.client)  # type:ignore


class Refunds(RefundsBase, ResourceListMixin):
    """Resource handler for the `/refunds` endpoint."""

    pass


class PaymentRefunds(RefundsBase, ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin):
    """Resource handler for the `/payments/:payment_id:/refunds` endpoint."""

    _payment = None

    def __init__(self, client, payment):
        self._payment = payment
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"payments/{self._payment.id}/refunds"  # type: ignore

    def get(self, resource_id: str, **params):
        self.validate_resource_id(resource_id, "Refund ID")
        return super().get(resource_id, **params)

    def delete(self, resource_id: str, **params):
        self.validate_resource_id(resource_id, "Refund ID")
        return super().delete(resource_id, **params)


class OrderRefunds(RefundsBase, ResourceCreateMixin, ResourceListMixin):
    """Resource handler for the `/orders/:order_id:/refunds` endpoint."""

    _order = None

    def __init__(self, client, order):
        super().__init__(client)
        self._order = order

    def get_resource_path(self) -> str:
        return f"orders/{self._order.id}/refunds"  # type: ignore

    def create(self, data: Optional[dict] = None, **params):
        """Create a refund for the order. When no data arg is given, a refund for all order lines is assumed."""
        if not data:
            data = {"lines": []}
        return super().create(data, **params)


class SettlementRefunds(RefundsBase, ResourceListMixin):
    """ResourceHandler for the `/settlements/:settlement_id:/refunds` endpoint."""

    _settlement = None

    def __init__(self, client, settlement):
        super().__init__(client)
        self._settlement = settlement

    def get_resource_path(self) -> str:
        return f"settlements/{self._settlement.id}/refunds"  # type: ignore


class ProfileRefunds(RefundsBase, ResourceBase):
    """
    Resource handler for the `/refunds?profileId=:profile_id:` endpoint.

    This is separate from the `Refunds` resource handler to make it easier to inject the profileId.
    """

    _profile = None

    def __init__(self, client, profile):
        self._profile = profile
        super().__init__(client)

    def list(self, **params) -> Refunds:
        # Set the profileId in the query params
        params.update({"profileId": self._profile.id})  # type: ignore
        return Refunds(self.client).list(**params)
