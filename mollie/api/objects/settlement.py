import warnings

from ..error import APIDeprecationWarning
from ..resources import SettlementCaptures, SettlementChargebacks, SettlementRefunds
from .base import ObjectBase


class Settlement(ObjectBase):
    STATUS_OPEN = "open"
    STATUS_PENDING = "pending"
    STATUS_PAIDOUT = "paidout"
    STATUS_FAILED = "failed"

    @classmethod
    def get_resource_class(cls, client):
        from ..resources import Settlements

        return Settlements(client)

    @property
    def id(self):
        return self._get_property("id")

    @property
    def reference(self):
        return self._get_property("reference")

    @property
    def created_at(self):
        return self._get_property("createdAt")

    @property
    def settled_at(self):
        return self._get_property("settledAt")

    @property
    def status(self):
        return self._get_property("status")

    @property
    def amount(self):
        return self._get_property("amount")

    @property
    def periods(self):
        return self._get_property("periods")

    @property
    def invoice_id(self):
        warnings.warn(
            "Using Settlement Invoice ID is deprecated, see "
            "https://docs.mollie.com/reference/v2/settlements-api/get-settlement",
            APIDeprecationWarning,
        )
        return self._get_property("invoiceId")

    # Additional methods

    def is_open(self):
        return self._get_property("status") == self.STATUS_OPEN

    def is_pending(self):
        return self._get_property("status") == self.STATUS_PENDING

    def is_canceled(self):
        return self._get_property("status") == self.STATUS_PAIDOUT

    def is_failed(self):
        return self._get_property("status") == self.STATUS_FAILED

    @property
    def payments(self):
        """Return the payments related to this settlement."""
        from ..resources import SettlementPayments

        return SettlementPayments(self.client, self)

    @property
    def refunds(self):
        """Return the refunds related to this settlement."""
        return SettlementRefunds(self.client, self)

    @property
    def chargebacks(self):
        """Return the chargebacks related to this settlement."""
        return SettlementChargebacks(self.client, self)

    @property
    def captures(self):
        """Return the captures related to this settlement."""
        return SettlementCaptures(self.client, self)

    def get_invoice(self):
        """Return the invoice related to this settlement."""
        url = self._get_link("invoice")
        return self.client.invoices.from_url(url)
