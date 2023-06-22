from .base import ObjectBase


class BalanceReport(ObjectBase):
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
