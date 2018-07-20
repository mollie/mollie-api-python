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
    def isOpen(self):
        return self.getProperty('status') == self.STATUS_OPEN

    @property
    def isPending(self):
        return self.getProperty('status') == self.STATUS_PENDING

    @property
    def isCanceled(self):
        return self.getProperty('status') == self.STATUS_CANCELED

    @property
    def isExpired(self):
        return self.getProperty('status') == self.STATUS_EXPIRED

    @property
    def isPaid(self):
        return 'paidAt' in self and len(self['paidAt']) > 0

    @property
    def isFailed(self):
        return self.getProperty('status') == self.STATUS_FAILED

    @property
    def hasRefunds(self):
        return len(self['_links']['refunds']) > 0

    @property
    def hasChargebacks(self):
        return len(self.getProperty('chargebacks')) > 0

    @property
    def hasSequenceTypeFirst(self):
        return self.getProperty('sequenceType') == self.SEQUENCETYPE_FIRST

    @property
    def hasSequenceTypeRecurring(self):
        return self.getProperty('sequenceType') == self.SEQUENCETYPE_RECURRING

    @property
    def getCheckoutUrl(self):
        if '_links' not in self:
            return None
        return self['_links']['checkout']

    @property
    def resource(self):
        return self.getProperty('resource')

    @property
    def id(self):
        return self.getProperty('id')

    @property
    def mode(self):
        return self.getProperty('mode')

    @property
    def createdAt(self):
        return self.getProperty('createdAt')

    @property
    def status(self):
        return self.getProperty('status')

    @property
    def isCancelable(self):
        return self['isCancelable']

    @property
    def paidAt(self):
        if 'paidAt' not in self:
            return None
        return self.getProperty('paidAt')

    @property
    def canceledAt(self):
        if 'canceledAt' not in self:
            return None
        return self.getProperty('canceledAt')

    @property
    def expiresAt(self):
        return self.getProperty('expiresAt')

    @property
    def expiredAt(self):
        if 'canceledAt' not in self:
            return None
        return self.getProperty('expiredAt')

    @property
    def failedAt(self):
        if 'canceledAt' not in self:
            return None
        return self.getProperty('failedAt')

    @property
    def amount(self):
        return self.getProperty('amount')

    @property
    def details(self):
        return self.getProperty('details')

    @property
    def profileId(self):
        return self.getProperty('profileId')

    @property
    def sequenceType(self):
        return self.getProperty('sequenceType')

    @property
    def redirectUrl(self):
        return self.getProperty('redirectUrl')

    @property
    def webhookUrl(self):
        return self.getProperty('webhookUrl')

    @property
    def description(self):
        return self.getProperty('description')

    @property
    def metadata(self):
        return self.getProperty('metadata')

    @property
    def settlementAmount(self):
        return self.getProperty('settlementAmount')

    @property
    def method(self):
        return self.getProperty('method')
