from .base import ObjectBase


class Payment(ObjectBase):
    @classmethod
    def get_resource_class(cls, client):
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
    def resource(self):
        return self._get_property("resource")

    @property
    def id(self):
        return self._get_property("id")

    @property
    def mode(self):
        return self._get_property("mode")

    @property
    def created_at(self):
        return self._get_property("createdAt")

    @property
    def status(self):
        return self._get_property("status")

    @property
    def is_cancelable(self):
        return self._get_property("isCancelable")

    @property
    def authorized_at(self):
        return self._get_property("authorizedAt")

    @property
    def paid_at(self):
        return self._get_property("paidAt")

    @property
    def canceled_at(self):
        return self._get_property("canceledAt")

    @property
    def expires_at(self):
        return self._get_property("expiresAt")

    @property
    def expired_at(self):
        return self._get_property("expiredAt")

    @property
    def failed_at(self):
        return self._get_property("failedAt")

    @property
    def amount(self):
        return self._get_property("amount")

    @property
    def amount_refunded(self):
        return self._get_property("amountRefunded")

    @property
    def amount_remaining(self):
        return self._get_property("amountRemaining")

    @property
    def amount_captured(self):
        return self._get_property("amountCaptured")

    @property
    def amount_chargedback(self):
        return self._get_property("amountChargedBack")

    @property
    def description(self):
        return self._get_property("description")

    @property
    def redirect_url(self):
        return self._get_property("redirectUrl")

    @property
    def webhook_url(self):
        return self._get_property("webhookUrl")

    @property
    def method(self):
        return self._get_property("method")

    @property
    def metadata(self):
        return self._get_property("metadata")

    @property
    def locale(self):
        return self._get_property("locale")

    @property
    def country_code(self):
        return self._get_property("countryCode")

    @property
    def profile_id(self):
        return self._get_property("profileId")

    @property
    def settlement_amount(self):
        return self._get_property("settlementAmount")

    @property
    def settlement_id(self):
        return self._get_property("settlementId")

    @property
    def customer_id(self):
        return self._get_property("customerId")

    @property
    def sequence_type(self):
        return self._get_property("sequenceType")

    @property
    def mandate_id(self):
        return self._get_property("mandateId")

    @property
    def subscription_id(self):
        return self._get_property("subscriptionId")

    @property
    def order_id(self):
        return self._get_property("orderId")

    @property
    def application_fee(self):
        return self._get_property("applicationFee")

    @property
    def details(self):
        return self._get_property("details")

    @property
    def routing(self):
        return self._get_property("routing")

    # documented _links

    @property
    def checkout_url(self):
        return self._get_link("checkout")

    @property
    def refunds(self):
        """Return the refunds related to this payment."""
        return self.client.payment_refunds.on(self).list()

    @property
    def chargebacks(self):
        """Return the chargebacks related to this payment."""
        return self.client.payment_chargebacks.on(self).list()

    @property
    def captures(self):
        """Return the captures related to this payment"""
        return self.client.captures.on(self).list()

    @property
    def settlement(self):
        """Return the settlement for this payment."""
        return self.client.settlements.get(self.settlement_id)

    @property
    def mandate(self):
        """Return the mandate for this payment."""
        return self.client.customer_mandates.with_parent_id(self.customer_id).get(self.mandate_id)

    @property
    def subscription(self):
        """Return the subscription for this payment."""
        return self.client.customer_subscriptions.with_parent_id(self.customer_id).get(self.subscription_id)

    @property
    def customer(self):
        """Return the customer for this payment."""
        return self.client.customers.get(self.customer_id)

    @property
    def order(self):
        """Return the order for this payment."""
        from .order import Order  # avoid circular import

        url = self._get_link("order")
        if url:
            resp = self.client.orders.perform_api_call(self.client.orders.REST_READ, url)
            return Order(resp, self.client)

    # additional methods

    def is_open(self):
        return self._get_property("status") == self.STATUS_OPEN

    def is_pending(self):
        return self._get_property("status") == self.STATUS_PENDING

    def is_canceled(self):
        return self._get_property("status") == self.STATUS_CANCELED

    def is_expired(self):
        return self._get_property("status") == self.STATUS_EXPIRED

    def is_failed(self):
        return self._get_property("status") == self.STATUS_FAILED

    def is_authorized(self):
        return self._get_property("status") == self.STATUS_AUTHORIZED

    def is_paid(self):
        return self._get_property("paidAt") is not None

    def has_refunds(self):
        return self._get_link("refunds") is not None

    def has_chargebacks(self):
        return self._get_link("chargebacks") is not None

    def has_captures(self):
        return self._get_link("captures") is not None

    def has_split_payments(self):
        return self._get_property("routing") is not None

    def can_be_refunded(self):
        return self._get_property("amountRemaining") is not None

    def has_sequence_type_first(self):
        return self._get_property("sequenceType") == self.SEQUENCETYPE_FIRST

    def has_sequence_type_recurring(self):
        return self._get_property("sequenceType") == self.SEQUENCETYPE_RECURRING
