from ..objects.refund import Refund
from .base import ResourceBase, ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin

__all__ = [
    "OrderRefunds",
    "PaymentRefunds",
    "ProfileRefunds",
    "Refunds",
    "SettlementRefunds",
]


class RefundsBase(ResourceBase):
    RESOURCE_ID_PREFIX = "re_"

    def get_resource_object(self, result):
        return Refund(result, self.client)


class Refunds(RefundsBase, ResourceListMixin):
    """Resource handle for /refunds/ endpoint."""

    pass


class PaymentRefunds(RefundsBase, ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin):
    """Resource handler for /payments/:paymentId:/refunds/ endpoint."""

    _payment = None

    def __init__(self, client, payment):
        super().__init__(client)
        self._payment = payment

    def get_resource_path(self):
        return f"payments/{self._payment.id}/refunds"

    def get(self, refund_id: str, **params):
        self.validate_resource_id(refund_id, "Refund ID")
        return super().get(refund_id, **params)

    def delete(self, refund_id: str, **params):
        self.validate_resource_id(refund_id, "Refund ID")
        return super().delete(refund_id, **params)


class OrderRefunds(RefundsBase, ResourceCreateMixin, ResourceListMixin):
    """Resource handler for /orders/:orderId:/refunds/ endpoint."""

    _order = None

    def __init__(self, client, order):
        super().__init__(client)
        self._order = order

    def get_resource_path(self):
        return f"orders/{self._order.id}/refunds"

    def create(self, data=None, **params):
        """Create a refund for the order. When no data arg is given, a refund for all order lines is assumed."""
        if not data:
            data = {"lines": []}
        return super().create(data, **params)


class SettlementRefunds(RefundsBase, ResourceListMixin):
    """ResourceHandler for /settlements/:settlementId:/refunds/ endpoint."""

    _settlement = None

    def __init__(self, client, settlement):
        super().__init__(client)
        self._settlement = settlement

    def get_resource_path(self):
        return f"settlements/{self._settlement.id}/refunds"


class ProfileRefunds(RefundsBase):
    _profile = None

    def __init__(self, client, profile):
        self._profile = profile
        super().__init__(client)

    def list(self, **params):
        # Set the profileId in the query params
        params.update({"profileId": self._profile.id})
        return Refunds(self.client).list(**params)
