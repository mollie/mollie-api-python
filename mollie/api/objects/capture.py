from .base import Base


class Capture(Base):
    @classmethod
    def get_resource_class(cls, client):
        from ..resources.captures import Captures
        return Captures(client)

    @property
    def id(self):
        return self._get_property('id')

    @property
    def mode(self):
        return self._get_property('mode')

    @property
    def amount(self):
        return self._get_property('amount')

    @property
    def settlement_amount(self):
        return self._get_property('settlementAmount')

    @property
    def payment_id(self):
        return self._get_property('paymentId')

    @property
    def shipment_id(self):
        return self._get_property('shipmentId')

    @property
    def settlement_id(self):
        return self._get_property('settlementId')

    @property
    def created_at(self):
        return self._get_property('createdAt')

    @property
    def payment(self):
        """Return the payment for this capture."""
        return self.client.payments.get(self.payment_id)

    @property
    def shipment(self):
        """Return the shipment for this capture."""
        from .shipment import Shipment
        url = self._get_link('shipment')

        if url:
            resp = self.client.orders.perform_api_call(self.client.orders.REST_READ, url)
            return Shipment(resp)

    @property
    def settlement(self):
        """Return the settlement for this capture."""
        return self.client.settlements.get(self.settlement_id)
