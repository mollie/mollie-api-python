from typing import Any

from .balance_report import BalanceReport
from .base import ObjectBase
from .list import PaginationList


class Balance(ObjectBase):
    @property
    def resource(self):
        return self._get_property("resource")

    @property
    def id(self):
        return self._get_property("id")

    @property
    def mode(self):
        return self._get_property("mode")

    @property
    def created_at(self):
        return self._get_property("createdAt")

    @property
    def currency(self):
        return self._get_property("currency")

    @property
    def status(self):
        return self._get_property("status")

    @property
    def transfer_frequency(self):
        return self._get_property("transferFrequency")

    @property
    def transfer_threshhold(self):
        return self._get_property("transferThreshold")

    @property
    def transfer_reference(self):
        return self._get_property("transferReference")

    @property
    def transfer_destination(self):
        return self._get_property("transferDestination")

    @property
    def available_amount(self):
        return self._get_property("availableAmount")

    @property
    def pending_amount(self):
        return self._get_property("pendingAmount")

    def get_report(self, **params: Any) -> BalanceReport:
        from ..resources import BalanceReports

        return BalanceReports(self.client, self).get_report(**params)

    def get_transactions(self, **params: Any) -> PaginationList:
        from ..resources import BalanceTransactions

        return BalanceTransactions(self.client, self).list(**params)
