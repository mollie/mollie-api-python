import pytest

from mollie.api.error import IdentifierError
from mollie.api.objects.invoice import Invoice

from .utils import assert_list_object

INVOICE_ID = "inv_xBEbP9rvAq"


def test_list_invoices(oauth_client, response):
    """Retrieve a list of existing invoices."""
    response.get("https://api.mollie.com/v2/invoices", "invoices_list")

    invoices = oauth_client.invoices.list()
    assert_list_object(invoices, Invoice)


def test_get_invoice(oauth_client, response):
    """Retrieve a single invoice."""
    response.get(f"https://api.mollie.com/v2/invoices/{INVOICE_ID}", "invoice_single")

    invoice = oauth_client.invoices.get(INVOICE_ID)
    assert isinstance(invoice, Invoice)
    assert invoice.id == INVOICE_ID
    assert invoice.resource == "invoice"
    assert invoice.id == "inv_xBEbP9rvAq"
    assert invoice.reference == "2016.10000"
    assert invoice.vat_number == "NL001234567B01"
    assert invoice.status == "open"
    assert invoice.issued_at == "2016-08-31"
    assert invoice.paid_at == "2016-09-01"
    assert invoice.due_at == "2016-09-14"
    assert invoice.net_amount == {"value": "45.00", "currency": "EUR"}
    assert invoice.vat_amount == {"value": "9.45", "currency": "EUR"}
    assert invoice.gross_amount == {"value": "54.45", "currency": "EUR"}
    assert invoice.lines == [
        {
            "period": "2016-09",
            "description": "iDEAL transactiekosten",
            "count": 100,
            "vatPercentage": 21,
            "amount": {"value": "45.00", "currency": "EUR"},
        }
    ]
    url = "https://www.mollie.com/merchant/download/invoice/xBEbP9rvAq/2ab44d60b35b1d06090bba955fa2c602"
    assert invoice.pdf == url


def test_get_invoice_invalid_id(oauth_client):
    with pytest.raises(IdentifierError) as excinfo:
        oauth_client.invoices.get("invalid")
    assert str(excinfo.value) == "Invalid invoice ID 'invalid', it should start with 'inv_'."
