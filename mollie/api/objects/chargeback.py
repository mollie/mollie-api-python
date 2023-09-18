import re

from .base import ObjectBase


class Chargeback(ObjectBase):
    @property
    def id(self):
        return self._get_property("id")

    @property
    def amount(self):
        return self._get_property("amount")

    @property
    def settlement_amount(self):
        return self._get_property("settlementAmount")

    @property
    def created_at(self):
        return self._get_property("createdAt")

    @property
    def reason(self):
        return self._get_property("reason")

    @property
    def reversed_at(self):
        return self._get_property("reversedAt")

    @property
    def payment_id(self):
        return self._get_property("paymentId")

    @property
    def settlement_id(self):
        """
        Return the settlement ID.

        It is extracted from the settlement link, since the id is not available as a real property.
        """
        url = self._get_link("settlement")
        if not url:
            return None

        match = re.findall(r"/settlements/(stl_[^/]+)/?$", url)
        if match:
            return match[0]

    def get_payment(self):
        """Return the Payment object related to this chargeback."""
        # TODO Use the embedded payment data, if available.
        return self.client.payments.get(self.payment_id)

    def get_settlement(self):
        """Return the Settlement object related to this chargeback, if available."""
        settlement_id = self.settlement_id
        if settlement_id is not None:
            return self.client.settlements.get(settlement_id)
