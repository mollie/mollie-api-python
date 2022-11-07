from typing import Optional

from ..objects.list import ObjectList
from ..objects.payment import Payment
from .base import (
    ResourceBase,
    ResourceCreateMixin,
    ResourceDeleteMixin,
    ResourceGetMixin,
    ResourceListMixin,
    ResourceUpdateMixin,
)

__all__ = [
    "CustomerPayments",
    "OrderPayments",
    "Payments",
    "ProfilePayments",
    "SettlementPayments",
    "SubscriptionPayments",
]


class PaymentsBase:
    RESOURCE_ID_PREFIX = "tr_"

    def get_resource_object(self, result: dict) -> Payment:
        from ..objects.payment import Payment

        return Payment(result, self.client)  # type: ignore


class Payments(
    PaymentsBase, ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin
):
    """Resource handler for the `/payments` endpoint."""

    def get(self, resource_id: str, **params):
        self.validate_resource_id(resource_id, "payment ID")
        return super().get(resource_id, **params)

    def delete(self, resource_id: str, **params):
        """Cancel payment and return the payment object.

        Deleting a payment causes the payment status to change to canceled.
        The updated payment object is returned.
        """
        self.validate_resource_id(resource_id, "payment ID")
        result = super().delete(resource_id, **params)
        return self.get_resource_object(result)

    def update(self, resource_id: str, data: Optional[dict] = None, **params):
        self.validate_resource_id(resource_id, "payment ID")
        return super().update(resource_id, data, **params)


class OrderPayments(PaymentsBase, ResourceCreateMixin):
    """Resource handler for the `/orders/:order_id:/payments` endpoint."""

    _order = None

    def __init__(self, client, order):
        self._order = order
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"orders/{self._order.id}/payments"  # type: ignore

    def list(self) -> ObjectList:
        """
        List the payments that might have been embedded in the related order.

        When you receive an EmbedError, you need to embed the payments in the parent order.
        """
        payments = self._order.get_embedded("payments")  # type: ignore

        data = {
            "_embedded": {
                "payments": payments,
            },
            "count": len(payments),
        }
        return ObjectList(data, Payment, self.client)


class CustomerPayments(PaymentsBase, ResourceCreateMixin, ResourceListMixin):
    """Resource handler for the `/customers/:customer_id:/payments` endpoint."""

    _customer = None

    def __init__(self, client, customer):
        self._customer = customer
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"customers/{self._customer.id}/payments"  # type: ignore


class SubscriptionPayments(PaymentsBase, ResourceListMixin):
    """Resource handler for the `/customers/:customer_id:/subscriptions/:subscription_id:/payments` endpoint."""

    _customer = None
    _subscription = None

    def __init__(self, client, customer, subscription):
        self._customer = customer
        self._subscription = subscription
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"customers/{self._customer.id}/subscriptions/{self._subscription.id}/payments"  # type: ignore


class SettlementPayments(PaymentsBase, ResourceListMixin):
    """Resource handler for the `/settlements/:settlement_id:/payments` endpoint."""

    _settlement = None

    def __init__(self, client, settlement):
        self._settlement = settlement
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"settlements/{self._settlement.id}/payments"  # type: ignore


class ProfilePayments(PaymentsBase, ResourceBase):
    """
    Resource handler for the `/payments?profileId=:profile_id:` endpoint.

    This is separate from the `Payments` resource handler to make it easier to inject the profileId.
    """

    _profile = None

    def __init__(self, client, profile):
        self._profile = profile
        super().__init__(client)

    def list(self, **params):
        # Set the profileId in the query params
        params.update({"profileId": self._profile.id})
        return Payments(self.client).list(**params)
