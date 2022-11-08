import pytest

from mollie.api.error import IdentifierError
from mollie.api.objects.customer import Customer
from mollie.api.objects.mandate import Mandate

from .utils import assert_list_object

CUSTOMER_ID = "cst_8wmqcHMN4U"
MANDATE_ID = "mdt_h3gAaD5zP"


def test_list_customer_mandates(client, response):
    """Retrieve a list of mandates."""
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/mandates", "customer_mandates_list")

    customer = client.customers.get(CUSTOMER_ID)
    mandates = customer.mandates.list()
    assert_list_object(mandates, Mandate)


def test_get_customer_mandate(client, response):
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/mandates/{MANDATE_ID}",
        "customer_mandate_single",
    )

    customer = client.customers.get(CUSTOMER_ID)
    mandate = customer.mandates.get(MANDATE_ID)
    assert isinstance(mandate, Mandate)
    assert mandate.id == MANDATE_ID
    assert mandate.resource == "mandate"
    assert mandate.status == "valid"
    assert mandate.method == "directdebit"
    assert mandate.details == {
        "consumerName": "John Doe",
        "consumerAccount": "NL55INGB0000000000",
        "consumerBic": "INGBNL2A",
    }
    assert mandate.mandate_reference == "YOUR-COMPANY-MD1380"
    assert mandate.signature_date == "2018-05-07"
    assert mandate.created_at == "2018-05-07T10:49:08+00:00"
    assert mandate.is_pending() is False
    assert mandate.is_valid() is True
    assert mandate.is_invalid() is False


def test_get_customer_mandate_invalid_id(client, response):
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")

    customer = client.customers.get(CUSTOMER_ID)
    with pytest.raises(IdentifierError) as excinfo:
        customer.mandates.get("invalid")
    assert str(excinfo.value) == "Invalid mandate ID 'invalid', it should start with 'mdt_'."


def test_customer_mandate_get_related_customer(client, response):
    """Retrieve a related customer object from a mandate."""
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/mandates/{MANDATE_ID}",
        "customer_mandate_single",
    )

    customer = client.customers.get(CUSTOMER_ID)
    mandate = customer.mandates.get(MANDATE_ID)
    customer = mandate.get_customer()
    assert isinstance(customer, Customer)
    assert customer.id == CUSTOMER_ID


def test_create_customer_mandate(client, response):
    """Create a new customer mandate."""
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.post(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/mandates", "customer_mandate_single")

    data = {
        "method": "directdebit",
        "consumerName": "John Doe",
        "consumerAccount": "NL55INGB0000000000",
        "consumerBic": "INGBNL2A",
        "signatureDate": "2018-05-07",
        "mandateReference": "YOUR-COMPANY-MD1380",
    }

    customer = client.customers.get(CUSTOMER_ID)
    mandate = customer.mandates.create(data)
    assert isinstance(mandate, Mandate)
    assert mandate.id == MANDATE_ID


def test_revoke_customer_mandate(client, response):
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.delete(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/mandates/{MANDATE_ID}",
        "empty",
        204,
    )

    customer = client.customers.get(CUSTOMER_ID)
    resp = customer.mandates.delete(MANDATE_ID)
    assert resp == {}


def test_revoke_customer_mandate_invalid_id(client, response):
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_new")

    customer = client.customers.get(CUSTOMER_ID)
    with pytest.raises(IdentifierError) as excinfo:
        customer.mandates.delete("invalid")
    assert str(excinfo.value) == "Invalid mandate ID 'invalid', it should start with 'mdt_'."
