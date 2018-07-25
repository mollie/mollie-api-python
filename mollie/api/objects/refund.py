from .base import Base


class Refund(Base):
    STATUS_QUEUED = 'queued'
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_REFUNDED = 'refunded'

    @property
    def is_queued(self):
        return self['status'] == self.STATUS_QUEUED

    @property
    def is_pending(self):
        return self['status'] == self.STATUS_PENDING

    @property
    def is_processing(self):
        return self['status'] == self.STATUS_PROCESSING

    @property
    def is_refunded(self):
        return self['status'] == self.STATUS_REFUNDED

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

    def cancel(self):
        try:
            url = self['_links']['self']['href']
        except KeyError:
            return None
        resp = self._resource.perform_api_call(self._resource.REST_DELETE, url)
        return Refund(resp)
