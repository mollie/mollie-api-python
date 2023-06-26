from typing import Any

from mollie.api.objects.balance import Balance
from mollie.api.objects.balance_report import BalanceReport
from mollie.api.objects.balance_transaction import BalanceTransaction
from mollie.api.resources.base import ResourceBase, ResourceGetMixin, ResourceListMixin


class Balances(ResourceGetMixin, ResourceListMixin):
    RESOURCE_ID_PREFIX: str = "bal_"

    @classmethod
    def validate_resource_id(cls, resource_id: str, name: str = "", message: str = "") -> None:
        """
        Validate the balance id.

        Valid references for balances are:
        - The string "primary"
        - A balance id, starting with "bal_"
        """
        exc_message = (
            f"Invalid balance ID '{resource_id}', it should start with '{cls.RESOURCE_ID_PREFIX}' or be the "
            f"string 'primary'."
        )

        if resource_id == "primary":
            return
        else:
            super().validate_resource_id(resource_id, message=exc_message)

    def get_resource_object(self, result: dict) -> Balance:
        from ..objects.balance import Balance

        return Balance(result, self.client)

    def get(self, resource_id: str, **params: Any) -> Balance:
        self.validate_resource_id(resource_id)
        return super().get(resource_id, **params)


class BalanceReports(ResourceBase):
    def get_resource_object(self, result: dict) -> BalanceReport:
        from ..objects.balance_report import BalanceReport

        return BalanceReport(result, self.client)

    def get_report(self, **params: Any) -> BalanceReport:
        path = self.get_resource_path()
        result = self.perform_api_call(self.REST_READ, path, params=params)
        return self.get_resource_object(result)


class BalanceTransactions(ResourceListMixin):
    def get_resource_object(self, result: dict) -> BalanceTransaction:
        from ..objects.balance_transaction import BalanceTransaction

        return BalanceTransaction(result, self.client)
