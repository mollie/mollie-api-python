from .base import Base


class Refund(Base):
    STATUS_QUEUED     = 'queued'
    STATUS_PENDING    = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_REFUNDED   = 'refunded'

    def is_queued(self):
        return self['status'] == self.STATUS_QUEUED

    def is_pending(self):
        return self['status'] == self.STATUS_PENDING

    def is_processing(self):
        return self['status'] == self.STATUS_PROCESSING

    def is_refunded(self):
        return self['status'] == self.STATUS_REFUNDED
