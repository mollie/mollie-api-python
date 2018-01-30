from .Base import Base


class Refund(Base):
    STATUS_QUEUED     = 'queued'
    STATUS_PENDING    = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_REFUNDED   = 'refunded'

    def isQueued(self):
        return self['status'] == self.STATUS_QUEUED

    def isPending(self):
        return self['status'] == self.STATUS_PENDING

    def isProcessing(self):
        return self['status'] == self.STATUS_PROCESSING

    def isRefunded(self):
        return self['status'] == self.STATUS_REFUNDED
