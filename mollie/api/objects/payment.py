from .base import Base
from .list import List


class Payment(Base):
    STATUS_OPEN = 'open'
    STATUS_PENDING = 'pending'
    STATUS_CANCELED = 'canceled'
    STATUS_EXPIRED = 'expired'
    STATUS_FAILED = 'failed'
    STATUS_PAID = 'paid'

    SEQUENCETYPE_ONEOFF = 'oneoff'
    SEQUENCETYPE_FIRST = 'first'
    SEQUENCETYPE_RECURRING = 'recurring'

    def is_open(self):
        return self._get_property('status') == self.STATUS_OPEN

    def is_pending(self):
        return self._get_property('status') == self.STATUS_PENDING

    def is_canceled(self):
        return self._get_property('status') == self.STATUS_CANCELED

    def is_expired(self):
        return self._get_property('status') == self.STATUS_EXPIRED

    def is_paid(self):
        return self._get_property('paidAt') is not None

    def is_failed(self):
        return self._get_property('status') == self.STATUS_FAILED

    def has_refunds(self):
        try:
            return self['_links']['refunds'] is not None
        except KeyError:
            return False

    def has_sequence_type_first(self):
        return self._get_property('sequenceType') == self.SEQUENCETYPE_FIRST

    def has_sequence_type_recurring(self):
        return self._get_property('sequenceType') == self.SEQUENCETYPE_RECURRING

    @property
    def checkout_url(self):
        try:
            return self['_links']['checkout']['href']
        except KeyError:
            return None

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
    def details(self):
        return self._get_property('details')

    @property
    def profile_id(self):
        return self._get_property('profileId')

    @property
    def sequence_type(self):
        return self._get_property('sequenceType')

    @property
    def redirect_url(self):
        return self._get_property('redirectUrl')

    @property
    def webhook_url(self):
        return self._get_property('webhookUrl')

    @property
    def description(self):
        return self._get_property('description')

    @property
    def metadata(self):
        return self._get_property('metadata')

    @property
    def settlement_amount(self):
        return self._get_property('settlementAmount')

    @property
    def method(self):
        return self._get_property('method')

    @property
    def customer_url(self):
        try:
            return self['_links']['customer']['href']
        except KeyError:
            return None

    @property
    def can_be_refunded(self):
        try:
            return self._get_property('amountRemaining') is not None
        except KeyError:
            return False

    @property
    def amount_refunded(self):
        try:
            return self['amountRefunded']
        except KeyError:
            return '0.0'

    @property
    def amount_remaining(self):
        try:
            return self['amountRemaining']
        except KeyError:
            return '0.0'

    @property
    def refunds(self):
        from .refund import Refund
        try:
            url = self['_links']['refunds']['href']
        except KeyError:
            return None
        resp = self._resource.perform_api_call(self._resource.REST_READ, url)
        return List(resp, Refund)

    @property
    def chargebacks(self):
        from .chargeback import Chargeback
        try:
            url = self['_links']['chargebacks']['href']
        except KeyError:
            return None
        resp = self._resource.perform_api_call(self._resource.REST_READ, url)
        return List(resp, Chargeback)
