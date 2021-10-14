import re

from ..error import DataConsistencyError
from .base import ObjectBase


class Chargeback(ObjectBase):
    @classmethod
    def get_resource_class(cls, client):
        from ..resources.chargebacks import Chargebacks

        return Chargebacks(client)

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
    def payment(self):
        """Return the Payment object related to this chargeback."""
        # TODO Use the embedded payment data, if available.
        return self.client.payments.get(self.payment_id)

    @property
    def settlement(self):
        """Return the Settlement object related to this chargeback, if available."""
        url = self._get_link("settlement")
        if not url:
            return None

        match = re.search(r"settlements/(stl_[a-zA-Z0-9]+)$", url)
        if not match:
            # This should never happen
            raise DataConsistencyError("Unable to extract the settlementId from settlement URL.")  # pragma: no cover

        settlement_id = match.group(1)
        return self.client.settlements.get(settlement_id)
