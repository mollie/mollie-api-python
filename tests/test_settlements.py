import pytest

from mollie.api.error import APIDeprecationWarning, IdentifierError
from mollie.api.objects.invoice import Invoice
from mollie.api.objects.settlement import Settlement
from mollie.api.resources import SettlementCaptures, SettlementChargebacks, SettlementPayments, SettlementRefunds
from mollie.api.resources.settlements import Settlements

from .utils import assert_list_object

SETTLEMENT_ID = "stl_jDk30akdN"
INVOICE_ID = "inv_xBEbP9rvAq"
BANK_REFERENCE = BANK_REFERENCE_SHORT = "1234.1804.03"
BANK_REFERENCE_LONG = "01234567.1804.03"
BANK_REFERENCE_FUTURE = "1234567890.1804.03"


def test_list_settlements(oauth_client, response):
    """Get a list of settlements."""
    response.get("https://api.mollie.com/v2/settlements", "settlements_list")

    settlements = oauth_client.settlements.list()
    assert_list_object(settlements, Settlement)


def test_settlement_get(oauth_client, response):
    """Retrieve a single settlement method by ID."""
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")

    settlement = oauth_client.settlements.get(SETTLEMENT_ID)
    assert isinstance(settlement, Settlement)

    assert isinstance(settlement.periods, dict)
    assert settlement.reference == "1234567.1804.03"
    assert settlement.created_at == "2018-04-06T06:00:01.0Z"
    assert settlement.settled_at == "2018-04-06T09:41:44.0Z"
    assert settlement.amount == {"currency": "EUR", "value": "39.75"}

    assert settlement.status == settlement.STATUS_OPEN
    assert settlement.is_open() is True
    assert settlement.is_canceled() is False
    assert settlement.is_failed() is False
    assert settlement.is_pending() is False

    assert isinstance(settlement.chargebacks, SettlementChargebacks)
    assert isinstance(settlement.payments, SettlementPayments)
    assert isinstance(settlement.refunds, SettlementRefunds)
    assert isinstance(settlement.captures, SettlementCaptures)


def test_settlement_get_next(oauth_client, response):
    """Retrieve the details of the current settlement that has not yet been paid out."""
    response.get("https://api.mollie.com/v2/settlements/next", "settlement_single")

    settlement = oauth_client.settlements.get("next")
    assert isinstance(settlement, Settlement)


def test_settlement_get_open(oauth_client, response):
    """Retrieve the details of the open balance of the organization."""
    response.get("https://api.mollie.com/v2/settlements/open", "settlement_single")

    settlement = oauth_client.settlements.get("open")
    assert isinstance(settlement, Settlement)


@pytest.mark.parametrize(
    "bank_reference",
    [
        BANK_REFERENCE_SHORT,
        BANK_REFERENCE_LONG,
        BANK_REFERENCE_FUTURE,
    ],
)
def test_get_settlement_by_bank_reference(oauth_client, response, bank_reference):
    response.get(f"https://api.mollie.com/v2/settlements/{bank_reference}", "settlement_single")

    settlement = oauth_client.settlements.get(bank_reference)
    assert isinstance(settlement, Settlement)


@pytest.mark.parametrize(
    "identifier",
    [
        "next",
        "open",
        SETTLEMENT_ID,
        BANK_REFERENCE,
    ],
)
def test_validate_settlement_id_valid_input(identifier):
    assert Settlements.validate_resource_id(identifier) is None


@pytest.mark.parametrize(
    "identifier",
    [
        None,
        "invalid",
    ],
)
def test_validate_settlement_id_invalid_input(identifier):
    with pytest.raises(IdentifierError) as excinfo:
        Settlements.validate_resource_id(identifier)
    assert str(excinfo.value) == (
        f"Invalid settlement ID '{identifier}', it should start with 'stl_', be 'next' or 'open', "
        "or contain a valid bank reference."
    )


def test_settlement_invoice_id_is_deprecated(oauth_client, response):
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")

    settlement = oauth_client.settlements.get(SETTLEMENT_ID)
    with pytest.warns(APIDeprecationWarning) as warnings:
        assert settlement.invoice_id == INVOICE_ID

    assert len(warnings) == 1
    assert str(warnings[0].message) == (
        "Using Settlement Invoice ID is deprecated, see "
        "https://docs.mollie.com/reference/v2/settlements-api/get-settlement"
    )


def test_settlement_get_related_invoice(oauth_client, response):
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")
    response.get(f"https://api.mollie.com/v2/invoices/{INVOICE_ID}", "invoice_single")

    settlement = oauth_client.settlements.get(SETTLEMENT_ID)
    invoice = settlement.get_invoice()
    assert isinstance(invoice, Invoice)
    assert invoice.id == INVOICE_ID
