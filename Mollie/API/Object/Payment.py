from .Base import *


class Payment(Base):
    STATUS_OPEN = 'open'
    STATUS_PENDING = 'pending'
    STATUS_CANCELLED = 'cancelled'
    STATUS_EXPIRED = 'expired'
    STATUS_PAID = 'paid'
    STATUS_PAIDOUT = 'paidout'
    STATUS_REFUNDED = 'refunded'

    def isOpen(self):
        return self['status'] == self.STATUS_OPEN

    def isPending(self):
        return self['status'] == self.STATUS_PENDING

    def isPaid(self):
        return 'paidDatetime' in self and self['paidDatetime']

    def getPaymentUrl(self):
        if 'links' not in self:
            return None
        return self['links']['paymentUrl']


class Refund(Base):
    pass