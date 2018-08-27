from .base import Base
from .list import List


class Refund(Base):
    STATUS_QUEUED = 'queued'
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_REFUNDED = 'refunded'

    # documented properties

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
    def lines(self):
        """
        A list of order lines.

        TODO: to support this, we need to implement the Order API first.
        """
        pass

    @property
    def payment_id(self):
        return self._get_property('paymentId')

    @property
    def order_id(self):
        return self._get_property('orderId')

    @property
    def created_at(self):
        return self._get_property('createdAt')

    # documented _links

    @property
    def payment(self):
        """Return the payment for this refund."""
        from .payment import Payment
        url = self._get_link('payment')
        if url:
            resp = self._resource.perform_api_call(self._resource.REST_READ, url)
            return List(resp, Payment)

    @property
    def settlement(self):
        """
        Return the settlement for this refund.

        TODO: Before we can return an Settlement object, we need to implement the Setlement API.
        """
        url = self._get_link('settlement')
        if url:
            resp = self._resource.perform_api_call(self._resource.REST_READ, url)
            return resp

    @property
    def order(self):
        """
        Return the payment for this refund.

        TODO: Before we can return an Order object, we need to implement the Orders API.
        """
        url = self._get_link('order')
        if url:
            resp = self._resource.perform_api_call(self._resource.REST_READ, url)
            return resp

    # additional methods

    def is_queued(self):
        return self.status == self.STATUS_QUEUED

    def is_pending(self):
        return self.status == self.STATUS_PENDING

    def is_processing(self):
        return self.status == self.STATUS_PROCESSING

    def is_refunded(self):
        return self.status == self.STATUS_REFUNDED
