from typing import TYPE_CHECKING, Any, Dict, Optional

from ..objects.customer import Customer
from ..objects.list import PaginationList
from ..objects.order import Order
from ..objects.payment import Payment
from ..objects.profile import Profile
from ..objects.subscription import Subscription
from .base import (
    ResourceBase,
    ResourceCreateMixin,
    ResourceDeleteMixin,
    ResourceGetMixin,
    ResourceListMixin,
    ResourceUpdateMixin,
)

if TYPE_CHECKING:
    from ..client import Client
    from ..objects.settlement import Settlement

__all__ = [
    "CustomerPayments",
    "OrderPayments",
    "Payments",
    "ProfilePayments",
    "SettlementPayments",
    "SubscriptionPayments",
]


class PaymentsBase(ResourceBase):
    RESOURCE_ID_PREFIX: str = "tr_"
    object_type = Payment


class Payments(
    PaymentsBase, ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin
):
    """Resource handler for the `/payments` endpoint."""

    def get(self, resource_id: str, **params: Any) -> Payment:
        self.validate_resource_id(resource_id, "payment ID")
        return super().get(resource_id, **params)

    def delete(self, resource_id: str, idempotency_key: str = "", **params: Any) -> dict:
        """Cancel payment and return the payment object.

        Deleting a payment causes the payment status to change to canceled.
        The updated payment object is returned.
        """
        self.validate_resource_id(resource_id, "payment ID")
        result = super().delete(resource_id, idempotency_key, **params)
        return Payment(result, self.client)

    def update(
        self, resource_id: str, data: Optional[Dict[str, Any]] = None, idempotency_key: str = "", **params: Any
    ) -> Payment:
        self.validate_resource_id(resource_id, "payment ID")
        return super().update(resource_id, data, idempotency_key, **params)


class OrderPayments(PaymentsBase, ResourceCreateMixin):
    """Resource handler for the `/orders/:order_id:/payments` endpoint."""

    _order: Order

    def __init__(self, client: "Client", order: Order) -> None:
        self._order = order
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"orders/{self._order.id}/payments"

    def list(self) -> PaginationList:
        """
        List the payments that might have been embedded in the related order.

        When you receive an EmbedError, you need to embed the payments in the parent order.
        """
        payments = self._order.get_embedded("payments")

        data = {
            "_embedded": {
                "payments": payments,
            },
            "count": len(payments),
        }
        return PaginationList(data, self, self.client)


class CustomerPayments(PaymentsBase, ResourceCreateMixin, ResourceListMixin):
    """Resource handler for the `/customers/:customer_id:/payments` endpoint."""

    _customer: Customer

    def __init__(self, client: "Client", customer: Customer) -> None:
        self._customer = customer
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"customers/{self._customer.id}/payments"


class SubscriptionPayments(PaymentsBase, ResourceListMixin):
    """Resource handler for the `/customers/:customer_id:/subscriptions/:subscription_id:/payments` endpoint."""

    _customer: Customer
    _subscription: Subscription

    def __init__(self, client: "Client", customer: Customer, subscription: Subscription) -> None:
        self._customer = customer
        self._subscription = subscription
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"customers/{self._customer.id}/subscriptions/{self._subscription.id}/payments"


class SettlementPayments(PaymentsBase, ResourceListMixin):
    """Resource handler for the `/settlements/:settlement_id:/payments` endpoint."""

    _settlement: "Settlement"

    def __init__(self, client: "Client", settlement: "Settlement") -> None:
        self._settlement = settlement
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"settlements/{self._settlement.id}/payments"


class ProfilePayments(PaymentsBase):
    """
    Resource handler for the `/payments?profileId=:profile_id:` endpoint.

    This is separate from the `Payments` resource handler to make it easier to inject the profileId.
    """

    _profile: Profile

    def __init__(self, client: "Client", profile: Profile) -> None:
        self._profile = profile
        super().__init__(client)

    def list(self, **params: Any) -> PaginationList:
        # Set the profileId in the query params
        params.update({"profileId": self._profile.id})
        return Payments(self.client).list(**params)
