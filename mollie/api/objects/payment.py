from .base import Base
from .list import List


class Payment(Base):
    @classmethod
    def get_resource_class(cls, client):
        from ..resources.payments import Payments
        return Payments(client)

    STATUS_OPEN = 'open'
    STATUS_PENDING = 'pending'
    STATUS_CANCELED = 'canceled'
    STATUS_EXPIRED = 'expired'
    STATUS_FAILED = 'failed'
    STATUS_PAID = 'paid'
    STATUS_AUTHORIZED = 'authorized'

    SEQUENCETYPE_ONEOFF = 'oneoff'
    SEQUENCETYPE_FIRST = 'first'
    SEQUENCETYPE_RECURRING = 'recurring'

    # Documented properties

    @property
    def resource(self):
        return self._get_property('resource')

    @property
    def id(self):
        return self._get_property('id')

    @property
    def mode(self):
        return self._get_property('mode')

    @property
    def created_at(self):
        return self._get_property('createdAt')

    @property
    def status(self):
        return self._get_property('status')

    @property
    def is_cancelable(self):
        return self._get_property('isCancelable')

    @property
    def authorized_at(self):
        return self._get_property('authorizedAt')

    @property
    def paid_at(self):
        return self._get_property('paidAt')

    @property
    def canceled_at(self):
        return self._get_property('canceledAt')

    @property
    def expires_at(self):
        return self._get_property('expiresAt')

    @property
    def expired_at(self):
        return self._get_property('expiredAt')

    @property
    def failed_at(self):
        return self._get_property('failedAt')

    @property
    def amount(self):
        return self._get_property('amount')

    @property
    def amount_refunded(self):
        return self._get_property('amountRefunded')

    @property
    def amount_remaining(self):
        return self._get_property('amountRemaining')

    @property
    def description(self):
        return self._get_property('description')

    @property
    def redirect_url(self):
        return self._get_property('redirectUrl')

    @property
    def webhook_url(self):
        return self._get_property('webhookUrl')

    @property
    def method(self):
        return self._get_property('method')

    @property
    def metadata(self):
        return self._get_property('metadata')

    @property
    def locale(self):
        return self._get_property('locale')

    @property
    def country_code(self):
        return self._get_property('countryCode')

    @property
    def profile_id(self):
        return self._get_property('profileId')

    @property
    def settlement_amount(self):
        return self._get_property('settlementAmount')

    @property
    def settlement_id(self):
        return self._get_property('settlementId')

    @property
    def customer_id(self):
        return self._get_property('customerId')

    @property
    def sequence_type(self):
        return self._get_property('sequenceType')

    @property
    def mandate_id(self):
        return self._get_property('mandateId')

    @property
    def subscription_id(self):
        return self._get_property('subscriptionId')

    @property
    def order_id(self):
        return self._get_property('orderId')

    @property
    def application_fee(self):
        return self._get_property('applicationFee')

    @property
    def details(self):
        return self._get_property('details')

    # documented _links

    @property
    def checkout_url(self):
        return self._get_link('checkout')

    @property
    def refunds(self):
        """Return the refunds related to this payment."""
        from .refund import Refund
        url = self._get_link('refunds')
        if url:
            resp = self._resource.perform_api_call(self._resource.REST_READ, url)
            return List(resp, Refund)

    @property
    def chargebacks(self):
        """Return the chargebacks related to this payment."""
        from .chargeback import Chargeback
        url = self._get_link('chargebacks')
        if url:
            resp = self._resource.perform_api_call(self._resource.REST_READ, url)
            return List(resp, Chargeback)

    @property
    def settlement(self):
        """
        Return the settlement for this payment.

        TODO: Before we can return a Settlement object, we need to implement the Settlement API.
        """
        url = self._get_link('settlement')
        if url:
            resp = self._resource.perform_api_call(self._resource.REST_READ, url)
            return resp

    @property
    def mandate(self):
        """Return the mandate for this payment."""
        from .mandate import Mandate
        url = self._get_link('mandate')
        if url:
            resp = self._resource.perform_api_call(self._resource.REST_READ, url)
            return Mandate(resp)

    @property
    def subscription(self):
        """Return the subscription for this payment."""
        from .subscription import Subscription
        url = self._get_link('subscription')
        if url:
            resp = self._resource.perform_api_call(self._resource.REST_READ, url)
            return Subscription(resp)

    @property
    def customer(self):
        """Return the customer for this payment."""
        from .customer import Customer
        url = self._get_link('customer')
        if url:
            resp = self._resource.perform_api_call(self._resource.REST_READ, url)
            return Customer(resp)

    @property
    def order(self):
        """Return the order for this payment. """
        from ..resources.orders import Order
        url = self._get_link('order')
        if url:
            resp = self._resource.perform_api_call(self._resource.REST_READ, url)
            return Order(resp, client=self.client)

    # additional methods

    def is_open(self):
        return self._get_property('status') == self.STATUS_OPEN

    def is_pending(self):
        return self._get_property('status') == self.STATUS_PENDING

    def is_canceled(self):
        return self._get_property('status') == self.STATUS_CANCELED

    def is_expired(self):
        return self._get_property('status') == self.STATUS_EXPIRED

    def is_failed(self):
        return self._get_property('status') == self.STATUS_FAILED

    def is_authorized(self):
        return self._get_property('status') == self.STATUS_AUTHORIZED

    def is_paid(self):
        return self._get_property('paidAt') is not None

    def has_refunds(self):
        return self._get_link('refunds') is not None

    def can_be_refunded(self):
        return self._get_property('amountRemaining') is not None

    def has_sequence_type_first(self):
        return self._get_property('sequenceType') == self.SEQUENCETYPE_FIRST

    def has_sequence_type_recurring(self):
        return self._get_property('sequenceType') == self.SEQUENCETYPE_RECURRING
