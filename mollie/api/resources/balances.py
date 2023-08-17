from typing import TYPE_CHECKING, Any

from mollie.api.objects.balance import Balance
from mollie.api.objects.balance_report import BalanceReport
from mollie.api.objects.balance_transaction import BalanceTransaction
from mollie.api.resources.base import ResourceBase, ResourceGetMixin, ResourceListMixin

if TYPE_CHECKING:
    from ..client import Client


class Balances(ResourceGetMixin, ResourceListMixin):
    RESOURCE_ID_PREFIX: str = "bal_"
    object_type = Balance

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

    def get(self, resource_id: str, **params: Any) -> Balance:
        self.validate_resource_id(resource_id)
        return super().get(resource_id, **params)


class BalanceReports(ResourceBase):
    _balance: "Balance"
    object_type = BalanceReport

    def __init__(self, client: "Client", balance: "Balance") -> None:
        self._balance = balance
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"balances/{self._balance.id}/report"

    def get_report(self, **params: Any) -> BalanceReport:
        path = self.get_resource_path()
        result = self.perform_api_call(self.REST_READ, path, params=params)
        return BalanceReport(result, self.client)


class BalanceTransactions(ResourceListMixin):
    _balance: "Balance"
    object_type = BalanceTransaction

    def __init__(self, client: "Client", balance: "Balance") -> None:
        self._balance = balance
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"balances/{self._balance.id}/transactions"
