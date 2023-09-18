from .base import ObjectBase
from .customer import Customer


class Payment(ObjectBase):
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

    @property
    def subscription_id(self):
        return self._get_property("subscriptionId")

    @property
    def cancel_url(self):
        return self._get_property("cancelUrl")

    # documented _links

    @property
    def checkout_url(self):
        return self._get_link("checkout")

    @property
    def changepaymentstate_url(self):
        return self._get_link("changePaymentState")

    @property
    def payonline_url(self):
        return self._get_link("payOnline")

    @property
    def refunds(self):
        """Return the refunds related to this payment."""
        from ..resources import PaymentRefunds

        return PaymentRefunds(self.client, self)

    @property
    def chargebacks(self):
        """Return the chargebacks related to this payment."""
        from ..resources import PaymentChargebacks

        return PaymentChargebacks(self.client, self)

    @property
    def captures(self):
        """Return the captures related to this payment"""
        from ..resources import PaymentCaptures

        return PaymentCaptures(self.client, self)

    @property
    def capture_before(self):
        return self._get_property("captureBefore")

    @property
    def capture_mode(self):
        return self._get_property("captureMode")

    @property
    def capture_delay(self):
        return self._get_property("captureDelay")

    def get_settlement(self):
        """Return the settlement for this payment."""
        if self.settlement_id:
            return self.client.settlements.get(self.settlement_id)

    def get_mandate(self):
        """Return the mandate for this payment."""
        if self.customer_id and self.mandate_id:
            # Setup a minimal Customer object without querying the API.
            customer = Customer({"id": self.customer_id}, self.client)
            return customer.mandates.get(self.mandate_id)

    def get_subscription(self):
        """
        Return the subscription for this payment.

        This is only available for recurring payments.
        """
        url = self._get_link("subscription")
        if url:
            from ..resources import CustomerSubscriptions

            customer = Customer({}, self.client)
            return CustomerSubscriptions(self.client, customer).from_url(url)

    def get_customer(self):
        """Return the customer for this payment."""
        if self.customer_id:
            return self.client.customers.get(self.customer_id)

    def get_order(self):
        """Return the order for this payment."""
        url = self._get_link("order")
        if url:
            return self.client.orders.from_url(url)

    # additional methods

    def is_open(self):
        return self.status == self.STATUS_OPEN

    def is_pending(self):
        return self.status == self.STATUS_PENDING

    def is_canceled(self):
        return self.status == self.STATUS_CANCELED

    def is_expired(self):
        return self.status == self.STATUS_EXPIRED

    def is_failed(self):
        return self.status == self.STATUS_FAILED

    def is_authorized(self):
        return self.status == self.STATUS_AUTHORIZED

    def is_paid(self):
        return self.paid_at is not None

    def has_refunds(self):
        return self._get_link("refunds") is not None

    def has_chargebacks(self):
        return self._get_link("chargebacks") is not None

    def has_captures(self):
        return self._get_link("captures") is not None

    def has_settlement(self):
        return self.settlement_id is not None

    def has_split_payments(self):
        return self.routing is not None

    def can_be_refunded(self):
        return self.amount_remaining is not None

    def has_sequence_type_first(self):
        return self.sequence_type == self.SEQUENCETYPE_FIRST

    def has_sequence_type_recurring(self):
        return self.sequence_type == self.SEQUENCETYPE_RECURRING
