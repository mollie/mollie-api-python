from typing import TYPE_CHECKING, Any

from .base import ObjectBase

if TYPE_CHECKING:
    from ..client import Client
    from ..resources import BalanceReports


class BalanceReport(ObjectBase):
    @classmethod
    def get_resource_class(cls, client: "Client", **kwargs: Any) -> "BalanceReports":
        from ..resources import BalanceReports

        balance = kwargs["balance"]
        return BalanceReports(client, balance)

    @property
    def resource(self):
        return self._get_property("resource")

    @property
    def balance_id(self):
        return self._get_property("balanceId")

    @property
    def time_zone(self):
        return self._get_property("timeZone")

    @property
    def from_(self):
        # 'from' is a reserverd word in Python, thus 'from_' is used.
        return self._get_property("from")

    @property
    def until(self):
        return self._get_property("until")

    @property
    def grouping(self):
        return self._get_property("grouping")

    @property
    def totals(self):
        return self._get_property("totals")
