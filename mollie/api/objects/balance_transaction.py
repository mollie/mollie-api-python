from .base import ObjectBase


class BalanceTransaction(ObjectBase):
    @classmethod
    def get_object_name(cls):
        # Overwrite get_object_name since BalanceTransactions gets returned by Mollie as balance_transactions.
        return "balance_transactions"

    @property
    def resource(self):
        return self._get_property("resource")

    @property
    def id(self):
        return self._get_property("id")

    @property
    def type(self):
        return self._get_property("type")

    @property
    def result_amount(self):
        return self._get_property("resultAmount")

    @property
    def initial_amount(self):
        return self._get_property("initialAmount")

    @property
    def deductions(self):
        return self._get_property("deductions")

    @property
    def created_at(self):
        return self._get_property("createdAt")

    @property
    def context(self):
        return self._get_property("context")
