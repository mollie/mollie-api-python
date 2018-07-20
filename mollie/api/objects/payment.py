from .base import Base


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

    @property
    def is_open(self):
        return self._get_property('status') == self.STATUS_OPEN

    @property
    def is_pending(self):
        return self._get_property('status') == self.STATUS_PENDING

    @property
    def is_canceled(self):
        return self._get_property('status') == self.STATUS_CANCELED

    @property
    def is_expired(self):
        return self._get_property('status') == self.STATUS_EXPIRED

    @property
    def is_paid(self):
        return 'paidAt' in self and len(self['paidAt']) > 0

    @property
    def is_failed(self):
        return self._get_property('status') == self.STATUS_FAILED

    @property
    def has_refunds(self):
        try:
            return len(self['_links']['refunds']) > 0
        except KeyError:
            return False

    @property
    def has_chargebacks(self):
        try:
            return len(self._get_property('chargebacks')) > 0
        except KeyError:
            return False

    @property
    def has_sequence_type_first(self):
        return self._get_property('sequenceType') == self.SEQUENCETYPE_FIRST

    @property
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
        return self['isCancelable']

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
    def value(self):
        return self.amount['value']

    @property
    def currency(self):
        return self.amount['currency']

    @property
    def order_id(self):
        if 'order_id' not in self.metadata:
            return None
        return self.metadata['order_id']

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
            False

    @property
    def get_amount_refunded(self):
        if self._get_property('amountRefunded'):
            return float(self._get_property('amountRefunded'))
        return 0.0

    @property
    def get_amount_remaining(self):
        if self.can_be_refunded:
            return float(self._get_property('amountRemaining'))
        return 0.0
