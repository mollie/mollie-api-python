from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from .base import ObjectBase

if TYPE_CHECKING:  # pragma: no cover
    from ..client import Client
    from ..resources.payments import Payments
    from ..typing import Amount
    from .customer import Customer
    from .list import Collection
    from .mandate import Mandate
    from .order import Order
    from .settlement import Settlement
    from .subscription import Subscription


class Payment(ObjectBase):
    @classmethod
    def get_resource_class(cls, client: Client) -> Payments:
        from ..resources.payments import Payments

        return Payments(client)

    STATUS_OPEN = "open"
    STATUS_PENDING = "pending"
    STATUS_CANCELED = "canceled"
    STATUS_EXPIRED = "expired"
    STATUS_FAILED = "failed"
    STATUS_PAID = "paid"
    STATUS_AUTHORIZED = "authorized"

    SEQUENCETYPE_ONEOFF = "oneoff"
    SEQUENCETYPE_FIRST = "first"
    SEQUENCETYPE_RECURRING = "recurring"

    # Documented properties

    @property
    def resource(self) -> str:
        return self._get_property("resource")

    @property
    def id(self) -> str:
        return self._get_property("id")

    @property
    def mode(self) -> str:
        return self._get_property("mode")

    @property
    def created_at(self) -> str:
        return self._get_property("createdAt")

    @property
    def status(self) -> str:
        return self._get_property("status")

    @property
    def is_cancelable(self) -> bool:
        return self._get_property("isCancelable")

    @property
    def authorized_at(self) -> Union[str, None]:
        return self._get_property("authorizedAt")

    @property
    def paid_at(self) -> Union[str, None]:
        return self._get_property("paidAt")

    @property
    def canceled_at(self) -> Union[str, None]:
        return self._get_property("canceledAt")

    @property
    def expires_at(self) -> Union[str, None]:
        return self._get_property("expiresAt")

    @property
    def expired_at(self) -> Union[str, None]:
        return self._get_property("expiredAt")

    @property
    def failed_at(self) -> Union[str, None]:
        return self._get_property("failedAt")

    @property
    def amount(self) -> dict[str, str]:
        return self._get_property("amount")

    @property
    def amount_refunded(self) -> Union[Amount, None]:
        return self._get_property("amountRefunded")

    @property
    def amount_remaining(self) -> Union[Amount, None]:
        return self._get_property("amountRemaining")

    @property
    def amount_captured(self) -> Union[Amount, None]:
        return self._get_property("amountCaptured")

    @property
    def amount_chargedback(self) -> Union[Amount, None]:
        return self._get_property("amountChargedBack")

    @property
    def description(self) -> str:
        return self._get_property("description")

    @property
    def redirect_url(self) -> Union[str, None]:
        return self._get_property("redirectUrl")

    @property
    def webhook_url(self) -> Union[str, None]:
        return self._get_property("webhookUrl")

    @property
    def method(self) -> str:
        return self._get_property("method")

    @property
    def metadata(self) -> Union[dict[Any, Any], None]:
        return self._get_property("metadata")

    @property
    def locale(self) -> Union[str, None]:
        return self._get_property("locale")

    @property
    def country_code(self) -> Union[str, None]:
        return self._get_property("countryCode")

    @property
    def profile_id(self) -> str:
        return self._get_property("profileId")

    @property
    def settlement_amount(self) -> Union[Amount, None]:
        return self._get_property("settlementAmount")

    @property
    def settlement_id(self) -> Union[str, None]:
        return self._get_property("settlementId")

    @property
    def customer_id(self) -> Union[str, None]:
        return self._get_property("customerId")

    @property
    def sequence_type(self) -> Union[str, None]:
        return self._get_property("sequenceType")

    @property
    def mandate_id(self) -> Union[str, None]:
        return self._get_property("mandateId")

    @property
    def subscription_id(self) -> Union[str, None]:
        return self._get_property("subscriptionId")

    @property
    def order_id(self) -> Union[str, None]:
        return self._get_property("orderId")

    @property
    def application_fee(self) -> Union[Amount, None]:
        return self._get_property("applicationFee")

    @property
    def details(self) -> Union[dict[Any, Any], None]:
        return self._get_property("details")

    @property
    def routing(self) -> Union[list[dict], None]:
        return self._get_property("routing")

    # documented _links

    @property
    def checkout_url(self) -> str:
        return self._get_link("checkout")

    @property
    def refunds(self) -> Collection:
        """Return the refunds related to this payment."""
        # TODO: refactor to use embedded data when available
        return self.client.payment_refunds.on(self).list()

    @property
    def chargebacks(self) -> Collection:
        """Return the chargebacks related to this payment."""
        # TODO: refactor to use embedded data when available
        return self.client.payment_chargebacks.on(self).list()

    @property
    def captures(self) -> Collection:
        """Return the captures related to this payment"""
        # TODO refactor this to omit the API call when has_captures is False.
        return self.client.captures.on(self).list()

    @property
    def settlement(self) -> Union[Settlement, None]:
        """Return the settlement for this payment."""
        if self.settlement_id:
            return self.client.settlements.get(self.settlement_id)
        return None

    @property
    def mandate(self) -> Union[Mandate, None]:
        """Return the mandate for this payment."""
        if self.customer_id and self.mandate_id:
            return self.client.customer_mandates.with_parent_id(self.customer_id).get(self.mandate_id)
        return None

    @property
    def subscription(self) -> Union[Subscription, None]:
        """Return the subscription for this payment."""
        if self.customer_id and self.subscription_id:
            return self.client.customer_subscriptions.with_parent_id(self.customer_id).get(self.subscription_id)
        return None

    @property
    def customer(self) -> Union[Customer, None]:
        """Return the customer for this payment."""
        if self.customer_id:
            return self.client.customers.get(self.customer_id)
        return None

    @property
    def order(self) -> Union[Order, None]:
        """Return the order for this payment."""
        # TODO: refactor this to use self.order_id
        from .order import Order  # avoid circular import

        url = self._get_link("order")
        if url:
            resp = self.client.orders.perform_api_call(self.client.orders.REST_READ, url)
            return Order(resp, self.client)
        return None

    # additional methods

    def is_open(self) -> bool:
        return self._get_property("status") == self.STATUS_OPEN

    def is_pending(self) -> bool:
        return self._get_property("status") == self.STATUS_PENDING

    def is_canceled(self) -> bool:
        return self._get_property("status") == self.STATUS_CANCELED

    def is_expired(self) -> bool:
        return self._get_property("status") == self.STATUS_EXPIRED

    def is_failed(self) -> bool:
        return self._get_property("status") == self.STATUS_FAILED

    def is_authorized(self) -> bool:
        return self._get_property("status") == self.STATUS_AUTHORIZED

    def is_paid(self) -> bool:
        return self._get_property("paidAt") is not None

    def has_refunds(self) -> bool:
        return self._get_link("refunds") is not None

    def has_chargebacks(self) -> bool:
        return self._get_link("chargebacks") is not None

    def has_captures(self) -> bool:
        return self._get_link("captures") is not None

    def has_split_payments(self) -> bool:
        return self._get_property("routing") is not None

    def can_be_refunded(self) -> bool:
        return self._get_property("amountRemaining") is not None

    def has_sequence_type_first(self) -> bool:
        return self._get_property("sequenceType") == self.SEQUENCETYPE_FIRST

    def has_sequence_type_recurring(self) -> bool:
        return self._get_property("sequenceType") == self.SEQUENCETYPE_RECURRING
