from .base import Base


class Refund(Base):
    STATUS_QUEUED = 'queued'
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_REFUNDED = 'refunded'

    def is_queued(self):
        return self.status == self.STATUS_QUEUED

    def is_pending(self):
        return self.status == self.STATUS_PENDING

    def is_processing(self):
        return self.status == self.STATUS_PROCESSING

    def is_refunded(self):
        return self.status == self.STATUS_REFUNDED

    @property
    def resource(self):
        return self._get_property('resource')

    @property
    def id(self):
        return self._get_property('id')

    @property
    def amount(self):
        return self._get_property('amount')

    @property
    def settlement_amount(self):
        return self._get_property('settlementAmount')

    @property
    def description(self):
        return self._get_property('description')

    @property
    def status(self):
        return self._get_property('status')

    @property
    def created_at(self):
        return self._get_property('createdAt')

    @property
    def payment_id(self):
        return self._get_property('paymentId')
