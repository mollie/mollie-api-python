from .base import Base
from .list import List
from .order_line import OrderLine


class Refund(Base):
    @classmethod
    def get_resource_class(cls, client):
        from ..resources.refunds import Refunds
        return Refunds(client)

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
        """Return the lines for this refund."""
        lines = self._get_property('lines') or []
        result = {
            '_embedded': {
                'lines': lines,
            },
            'count': len(lines),
        }
        return List(result, OrderLine, client=self.client)

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
            return Payment(resp)

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
        """Return the order for this refund."""
        from ..resources.orders import Order

        url = self._get_link('order')
        if url:
            resp = self._resource.perform_api_call(self._resource.REST_READ, url)
            return Order(resp, client=self.client)

    # additional methods

    def is_queued(self):
        return self.status == self.STATUS_QUEUED

    def is_pending(self):
        return self.status == self.STATUS_PENDING

    def is_processing(self):
        return self.status == self.STATUS_PROCESSING

    def is_refunded(self):
        return self.status == self.STATUS_REFUNDED
