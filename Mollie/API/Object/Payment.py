from .Base import Base


class Payment(Base):
    STATUS_OPEN         = 'open'
    STATUS_PENDING      = 'pending'
    STATUS_CANCELLED    = 'cancelled'
    STATUS_EXPIRED      = 'expired'
    STATUS_PAID         = 'paid'
    STATUS_PAIDOUT      = 'paidout'
    STATUS_REFUNDED     = 'refunded'
    STATUS_FAILED       = 'failed'
    STATUS_CHARGED_BACK = 'charged_back'

    def isOpen(self):
        return self['status'] == self.STATUS_OPEN

    def isPending(self):
        return self['status'] == self.STATUS_PENDING

    def isCancelled(self):
        return self['status'] == self.STATUS_CANCELLED

    def isExpired(self):
        return self['status'] == self.STATUS_EXPIRED

    def isPaid(self):
        return 'paidDatetime' in self and len(self['paidDatetime']) > 0

    def isPaidout(self):
        return self['status'] == self.STATUS_PAIDOUT

    def isRefunded(self):
        return self['status'] == self.STATUS_REFUNDED

    def isFailed(self):
        return self['status'] == self.STATUS_FAILED

    def isChargedBack(self):
        return self['status'] == self.STATUS_CHARGED_BACK

    def getPaymentUrl(self):
        if 'links' not in self:
            return None
        return self['links']['paymentUrl']
