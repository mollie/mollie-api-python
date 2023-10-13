from .base import ObjectBase
from .list import ObjectList
from .order_line import OrderLine


class Refund(ObjectBase):
    STATUS_QUEUED = "queued"
    STATUS_PENDING = "pending"
    STATUS_PROCESSING = "processing"
    STATUS_REFUNDED = "refunded"

    # documented properties

    @property
    def resource(self):
        return self._get_property("resource")

    @property
    def id(self):
        return self._get_property("id")

    @property
    def amount(self):
        return self._get_property("amount")

    @property
    def settlement_id(self):
        return self._get_property("settlementId")

    @property
    def settlement_amount(self):
        return self._get_property("settlementAmount")

    @property
    def description(self):
        return self._get_property("description")

    @property
    def status(self):
        return self._get_property("status")

    @property
    def lines(self):
        """Return the lines for this refund."""
        lines = self._get_property("lines") or []
        result = {
            "_embedded": {
                "lines": lines,
            },
            "count": len(lines),
        }
        return ObjectList(result, OrderLine, self.client)

    @property
    def payment_id(self):
        return self._get_property("paymentId")

    @property
    def order_id(self):
        return self._get_property("orderId")

    @property
    def created_at(self):
        return self._get_property("createdAt")

    @property
    def metadata(self):
        return self._get_property("metadata")

    # documented _links

    def get_payment(self):
        """Return the payment for this refund."""
        return self.client.payments.get(self.payment_id)

    def get_settlement(self):
        """Return the settlement for this refund."""
        if self.settlement_id:
            return self.client.settlements.get(self.settlement_id)
        return None

    def get_order(self):
        """Return the order for this refund."""
        if self.order_id:
            return self.client.orders.get(self.order_id)
        return None

    # additional methods

    def is_queued(self):
        return self.status == self.STATUS_QUEUED

    def is_pending(self):
        return self.status == self.STATUS_PENDING

    def is_processing(self):
        return self.status == self.STATUS_PROCESSING

    def is_refunded(self):
        return self.status == self.STATUS_REFUNDED
