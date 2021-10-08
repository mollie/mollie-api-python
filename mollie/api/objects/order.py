from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Union

from ..error import EmbedNotFound
from ..resources.order_lines import OrderLines
from ..resources.order_payments import OrderPayments
from ..resources.order_refunds import OrderRefunds
from ..resources.shipments import Shipments
from .base import ObjectBase
from .list import Collection
from .order_line import OrderLine
from .payment import Payment

if TYPE_CHECKING:  # pragma: no cover
    from ..client import Client
    from ..resources.orders import Orders
    from ..typing import Amount
    from .refund import Refund
    from .shipment import Shipment


class Order(ObjectBase):
    requested_embeds = None

    def __init__(self, data: dict, client: Optional[Client] = None, requested_embeds: Optional[list] = None) -> None:
        super().__init__(data, client)
        self.requested_embeds = requested_embeds

    def _has_embed(self, embed_name: str) -> bool:
        if self.requested_embeds and embed_name in self.requested_embeds:
            return True
        return False

    @classmethod
    def get_resource_class(cls, client: Client) -> Orders:
        from ..resources.orders import Orders

        return Orders(client)

    STATUS_CREATED = "created"
    STATUS_PAID = "paid"
    STATUS_AUTHORIZED = "authorized"
    STATUS_CANCELED = "canceled"
    STATUS_SHIPPING = "shipping"
    STATUS_COMPLETED = "completed"
    STATUS_EXPIRED = "expired"

    @property
    def id(self) -> str:
        return self._get_property("id")

    @property
    def resource(self) -> str:
        return self._get_property("resource")

    @property
    def profile_id(self) -> str:
        return self._get_property("profileId")

    @property
    def method(self) -> str:
        return self._get_property("method")

    @property
    def mode(self) -> str:
        return self._get_property("mode")

    @property
    def amount(self) -> Union[Amount, None]:
        return self._get_property("amount")

    @property
    def amount_captured(self) -> Union[Amount, None]:
        return self._get_property("amountCaptured")

    @property
    def amount_refunded(self) -> Union[Amount, None]:
        return self._get_property("amountRefunded")

    @property
    def status(self) -> str:
        return self._get_property("status")

    @property
    def is_cancelable(self) -> bool:
        return self._get_property("isCancelable")

    @property
    def billing_address(self) -> dict[str, str]:
        return self._get_property("billingAddress")

    @property
    def consumer_date_of_birth(self) -> Union[str, None]:
        return self._get_property("consumerDateOfBirth")

    @property
    def order_number(self) -> str:
        return self._get_property("orderNumber")

    @property
    def shipping_address(self) -> dict[str, str]:
        return self._get_property("shippingAddress")

    @property
    def locale(self) -> str:
        return self._get_property("locale")

    @property
    def metadata(self) -> Union[dict[Any, Any], None]:
        return self._get_property("metadata")

    @property
    def redirect_url(self) -> Union[str, None]:
        return self._get_property("redirectUrl")

    @property
    def webhook_url(self) -> Union[str, None]:
        return self._get_property("webhookUrl")

    @property
    def created_at(self) -> str:
        return self._get_property("createdAt")

    @property
    def expires_at(self) -> Union[str, None]:
        return self._get_property("expiresAt")

    @property
    def expired_at(self) -> Union[str, None]:
        return self._get_property("expiredAt")

    @property
    def paid_at(self) -> Union[str, None]:
        return self._get_property("paidAt")

    @property
    def authorized_at(self) -> Union[str, None]:
        return self._get_property("authorizedAt")

    @property
    def canceled_at(self) -> Union[str, None]:
        return self._get_property("canceledAt")

    @property
    def completed_at(self) -> Union[str, None]:
        return self._get_property("completedAt")

    # documented _links

    @property
    def checkout_url(self) -> Union[str, None]:
        return self._get_link("checkout")

    # additional methods

    def is_created(self) -> bool:
        return self._get_property("status") == self.STATUS_CREATED

    def is_paid(self) -> bool:
        return self._get_property("status") == self.STATUS_PAID

    def is_authorized(self) -> bool:
        return self._get_property("status") == self.STATUS_AUTHORIZED

    def is_canceled(self) -> bool:
        return self._get_property("status") == self.STATUS_CANCELED

    def is_shipping(self) -> bool:
        return self._get_property("status") == self.STATUS_SHIPPING

    def is_completed(self) -> bool:
        return self._get_property("status") == self.STATUS_COMPLETED

    def is_expired(self) -> bool:
        return self._get_property("status") == self.STATUS_EXPIRED

    def has_refunds(self) -> bool:
        return self._get_link("refunds") is not None

    def has_shipments(self) -> bool:
        return self._get_link("shipments") is not None

    def create_refund(self, data: Optional[dict[Any, Any]] = None, **params: Optional[dict[str, Any]]) -> Refund:
        """Create a refund for the order. When no data arg is given, a refund for all order lines is assumed."""
        if data is None:
            data = {"lines": []}
        refund = OrderRefunds(self.client).on(self).create(data, **params)
        return refund

    def cancel_lines(self, data: Optional[dict[Any, Any]] = None) -> dict[str, str]:
        """Cancel the lines given. When no lines are given, cancel all the lines.

        Canceling an order line causes the order line status to change to canceled.
        An empty dictionary will be returned.
        """
        from ..resources.order_lines import OrderLines

        if data is None:
            data = {"lines": []}
        canceled = OrderLines(self.client).on(self).delete(data)
        return canceled

    @property
    def refunds(self) -> Collection:
        # TODO: refactor to use embedded data when available
        return OrderRefunds(self.client).on(self).list()

    @property
    def lines(self) -> Collection:
        lines = self._get_property("lines") or []
        result = {
            "_embedded": {
                "lines": lines,
            },
            "count": len(lines),
        }
        return Collection(result, OrderLine, self.client)

    def update_line(self, resource_id: str, data: dict[str, str]) -> OrderLine:
        """Update a line for an order."""
        return OrderLines(self.client).on(self).update(resource_id, data)

    @property
    def shipments(self) -> Collection:
        """Retrieve all shipments for an order."""
        # TODO: refactor to use embedded data when available
        return Shipments(self.client).on(self).list()

    def create_shipment(self, data: dict[Any, Any] = None) -> Shipment:
        """Create a shipment for an order. When no data arg is given, a shipment for all order lines is assumed."""
        if data is None:
            data = {"lines": []}
        return Shipments(self.client).on(self).create(data)

    def get_shipment(self, resource_id: str) -> Shipment:
        """Retrieve a single shipment by a shipment's ID."""
        return Shipments(self.client).on(self).get(resource_id)

    def update_shipment(self, resource_id: str, data: dict[Any, Any]) -> Shipment:
        """Update the tracking information of a shipment."""
        return Shipments(self.client).on(self).update(resource_id, data)

    @property
    def payments(self) -> Collection:
        # TODO: refactor to use embedded data when available, warn about doing additional API calls
        if not self._has_embed("payments"):
            raise EmbedNotFound("payments")

        try:
            payments = self["_embedded"]["payments"]
        except KeyError:
            # No data available at API
            payments = []

        result = {
            "_embedded": {
                "payments": payments,
            },
            "count": len(payments),
        }
        return Collection(result, Payment, self.client)

    def create_payment(self, data: dict[Any, Any]) -> Payment:
        """Creates a new payment object for an order."""
        return OrderPayments(self.client).on(self).create(data)
