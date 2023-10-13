from .base import ObjectBase


class Capture(ObjectBase):
    @property
    def id(self):
        return self._get_property("id")

    @property
    def mode(self):
        return self._get_property("mode")

    @property
    def amount(self):
        return self._get_property("amount")

    @property
    def settlement_amount(self):
        return self._get_property("settlementAmount")

    @property
    def payment_id(self):
        return self._get_property("paymentId")

    @property
    def shipment_id(self):
        return self._get_property("shipmentId")

    @property
    def settlement_id(self):
        return self._get_property("settlementId")

    @property
    def created_at(self):
        return self._get_property("createdAt")

    def get_payment(self):
        """Return the payment for this capture."""
        # TODO Use the embedded payment data, if available.
        return self.client.payments.get(self.payment_id)

    def get_shipment(self):
        """Return the shipment for this capture."""
        url = self._get_link("shipment")
        if url:
            from ..resources import OrderShipments
            from .order import Order

            order = Order({}, self.client)
            return OrderShipments(self.client, order).from_url(url)

    def get_settlement(self):
        """Return the settlement for this capture."""
        return self.client.settlements.get(self.settlement_id)
