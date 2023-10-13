import pytest

from mollie.api.error import IdentifierError
from mollie.api.objects.customer import Customer
from mollie.api.objects.mandate import Mandate
from mollie.api.objects.payment import Payment
from mollie.api.objects.subscription import Subscription

from .utils import assert_list_object

CUSTOMER_ID = "cst_8wmqcHMN4U"


def test_create_customer(client, response):
    """Create a new customer."""
    response.post("https://api.mollie.com/v2/customers", "customer_new")

    customer = client.customers.create(
        {
            "name": "Customer A",
            "email": "customer@example.org",
            "locale": "nl_NL",
        }
    )
    assert isinstance(customer, Customer)
    assert customer.id == CUSTOMER_ID


def test_update_customer(client, response):
    """Update an existing customer."""
    response.patch(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_updated")

    updated_customer = client.customers.update(
        CUSTOMER_ID,
        {
            "name": "Updated Customer A",
            "email": "updated-customer@example.org",
        },
    )
    assert isinstance(updated_customer, Customer)
    assert updated_customer.name == "Updated Customer A"
    assert updated_customer.email == "updated-customer@example.org"


def test_update_customer_invalid_id(client):
    data = {}
    with pytest.raises(IdentifierError) as excinfo:
        client.customers.update("invalid", data)
    assert str(excinfo.value) == "Invalid customer ID 'invalid', it should start with 'cst_'."


def test_delete_customer(client, response):
    """Delete a customer."""
    response.delete(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "empty")

    deleted_customer = client.customers.delete("cst_8wmqcHMN4U")
    assert deleted_customer == {}


def test_delete_customer_invalid_id(client):
    with pytest.raises(IdentifierError) as excinfo:
        client.customers.delete("invalid")
    assert str(excinfo.value) == "Invalid customer ID 'invalid', it should start with 'cst_'."


def test_list_customers(client, response):
    """Retrieve a list of existing customers."""
    response.get("https://api.mollie.com/v2/customers", "customers_list")

    customers = client.customers.list()
    assert_list_object(customers, Customer)


def test_get_customer(client, response):
    """Retrieve a single customer."""
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_new")

    customer = client.customers.get(CUSTOMER_ID)
    assert isinstance(customer, Customer)
    assert customer.id == CUSTOMER_ID
    assert customer.name == "Customer A"
    assert customer.email == "customer@example.org"
    assert customer.locale == "nl_NL"
    assert customer.metadata == {"orderId": "12345"}
    assert customer.mode == "test"
    assert customer.resource == "customer"
    assert customer.created_at == "2018-04-06T13:10:19.0Z"
    assert customer.subscriptions is not None
    assert customer.mandates is not None
    assert customer.payments is not None


def test_get_customer_invalid_id(client):
    with pytest.raises(IdentifierError) as excinfo:
        client.customers.get("invalid")
    assert str(excinfo.value) == "Invalid customer ID 'invalid', it should start with 'cst_'."


def test_customer_get_related_mandates(client, response):
    """Retrieve related mandates for a customer."""
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/mandates", "customer_mandates_list")

    customer = client.customers.get(CUSTOMER_ID)
    mandates = customer.mandates.list()
    assert_list_object(mandates, Mandate)


def test_customer_get_related_subscriptions(client, response):
    """Retrieve related subscriptions for a customer."""
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions", "customer_subscriptions_list")

    customer = client.customers.get(CUSTOMER_ID)
    subscriptions = customer.subscriptions.list()
    assert_list_object(subscriptions, Subscription)


def test_customer_get_related_payments(client, response):
    """Retrieve related payments for a customer."""
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/payments", "customer_payments_multiple")

    customer = client.customers.get(CUSTOMER_ID)
    payments = customer.payments.list()
    assert_list_object(payments, Payment)
