import re

from ..error import DataConsistencyError
from .base import ObjectBase


class Capture(ObjectBase):
    @classmethod
    def get_resource_class(cls, client):
        from ..resources.captures import Captures

        return Captures(client)

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

    @property
    def payment(self):
        """Return the payment for this capture."""
        # TODO Use the embedded payment data, if avalable.
        return self.client.payments.get(self.payment_id)

    @property
    def shipment(self):
        """Return the shipment for this capture."""
        # Dev note: this would be a lot cleaner if we had access to the orderId directly.
        url = self._get_link("shipment")
        if not url:
            return None

        match = re.search(r"orders/(ord_[a-zA-Z0-9]+)/shipments", url)
        if not match:
            # This should never happen
            raise DataConsistencyError("Unable to extract the orderId from shipment URL.")  # pragma: no cover

        order_id = match.group(1)
        return self.client.shipments.with_parent_id(order_id).get(self.shipment_id)

    @property
    def settlement(self):
        """Return the settlement for this capture."""
        return self.client.settlements.get(self.settlement_id)
