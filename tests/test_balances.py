from unittest.mock import patch

import pytest

from mollie.api.error import IdentifierError
from mollie.api.objects.balance import Balance
from mollie.api.objects.balance_report import BalanceReport
from mollie.api.objects.balance_transaction import BalanceTransaction

from .utils import assert_list_object

BALANCE_ID = "bal_gVMhHKqSSRYJyPsuoPNFH"
BALANCE_TRANSACTION_ID = "baltr_QM24QwzUWR4ev4Xfgyt29A"


def test_list_balances(client, response):
    """Get a list of balances."""
    response.get("https://api.mollie.com/v2/balances", "balances_list")

    balances = client.balances.list()
    assert_list_object(balances, Balance)


def test_get_specific_balance(client, response):
    """Get a specific balance"""
    response.get(f"https://api.mollie.com/v2/balances/{BALANCE_ID}", "balance_single")
    balance = client.balances.get(BALANCE_ID)

    assert isinstance(balance, Balance)

    assert balance.resource == "balance"
    assert balance.id == BALANCE_ID
    assert balance.mode == "test"
    assert balance.created_at == "2019-01-10T10:23:41+00:00"
    assert balance.currency == "EUR"
    assert balance.status == "active"
    assert balance.available_amount == {"value": "905.25", "currency": "EUR"}
    assert balance.pending_amount == {"value": "0.00", "currency": "EUR"}

    assert balance.transfer_frequency == "twice-a-month"
    assert balance.transfer_threshhold == {"value": "5.00", "currency": "EUR"}

    assert balance.transfer_reference == "Mollie payout"
    assert balance.transfer_destination == {
        "type": "bank-account",
        "beneficiaryName": "Jack Bauer",
        "bankAccount": "NL53INGB0654422370",
        "bankAccountId": "bnk_jrty3f",
    }


def test_get_primary_balance(client, response):
    """Get the primary balance"""
    response.get("https://api.mollie.com/v2/balances/primary", "balance_single")
    balance = client.balances.get("primary")

    assert balance.id == BALANCE_ID
    assert isinstance(balance, Balance)


def test_get_balance_report(client, response):
    """Get a balance report."""
    response.get(f"https://api.mollie.com/v2/balances/{BALANCE_ID}", "balance_single")
    response.get(f"https://api.mollie.com/v2/balances/{BALANCE_ID}/report", "balance_report_single")

    balance = client.balances.get(BALANCE_ID)
    balance_report = balance.get_report()
    assert isinstance(balance_report, BalanceReport)

    assert balance_report.resource == "balance-report"
    assert balance_report.balance_id == BALANCE_ID
    assert balance_report.time_zone == "Europe/Amsterdam"
    assert balance_report.from_ == "2021-01-01"
    assert balance_report.until == "2021-01-31"
    assert balance_report.grouping == "transaction-categories"
    assert balance_report.totals == {"some_data": "some_data"}


def test_get_balance_transactions(client, response):
    """Get a list of balance transactions."""
    response.get(f"https://api.mollie.com/v2/balances/{BALANCE_ID}", "balance_single")
    response.get(f"https://api.mollie.com/v2/balances/{BALANCE_ID}/transactions", "balance_transactions_list")

    balance = client.balances.get(BALANCE_ID)
    balance_transactions = balance.get_transactions()
    assert_list_object(balance_transactions, BalanceTransaction)

    balance_transaction = balance_transactions[0]
    assert balance_transaction.resource == "balance_transaction"
    assert balance_transaction.id == BALANCE_TRANSACTION_ID
    assert balance_transaction.type == "refund"
    assert balance_transaction.result_amount == {"value": "-10.25", "currency": "EUR"}
    assert balance_transaction.initial_amount == {"value": "-10.00", "currency": "EUR"}
    assert balance_transaction.deductions == {"value": "-0.25", "currency": "EUR"}

    assert balance_transaction.created_at == "2021-01-10T12:06:28+00:00"
    assert balance_transaction.context == {"paymentId": "tr_7UhSN1zuXS", "refundId": "re_4qqhO89gsT"}


def test_get_balance_transactions_with_params(client, response):
    """Get a list of balance transactions with parameters."""
    response.get(f"https://api.mollie.com/v2/balances/{BALANCE_ID}", "balance_single")

    balance = client.balances.get(BALANCE_ID)
    params = {"limit": 5, "sort": "asc"}

    with patch("mollie.api.resources.base.ResourceListMixin.perform_api_call") as mock_perform_api_call:
        balance.get_transactions(**params)

        # Assert perform_api_call was called
        mock_perform_api_call.assert_called_once()

        # Extract the parameters passed to perform_api_call
        _, called_kwargs = mock_perform_api_call.call_args
        called_params = called_kwargs.get("params")

        # Assert the params are what we expect
        assert called_params == params


def test_get_balance_invalid_id(client):
    """Test that the balance ID is validated upon retrieving a balance.

    It is invalid if it does not start with 'bal_' or is the string 'primary'.
    """
    with pytest.raises(IdentifierError) as excinfo:
        client.balances.get("invalid")
    assert (
        str(excinfo.value) == "Invalid balance ID 'invalid', it should start with 'bal_' or be the string 'primary'."
    )

    assert (
        client.balances.validate_resource_id("bal_1337") is None
    ), "A correct balance ID should not raise a validation error"
    assert (
        client.balances.validate_resource_id("primary") is None
    ), "A correct balance ID should not raise a validation error"
