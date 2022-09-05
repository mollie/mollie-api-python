import re

import pytest

from mollie.api.error import RemovedIn215Warning
from mollie.api.objects.payment import Payment

from .utils import assert_list_object

CUSTOMER_ID = "cst_8wmqcHMN4U"


def test_list_customer_payments_by_parent_id(client, response):
    """Retrieve a list of payments related to a customer id."""
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/payments", "customer_payments_multiple")

    payments = client.payments.with_parent_id(CUSTOMER_ID).list()
    assert_list_object(payments, Payment)


def test_list_customer_payments_by_parent_object(client, response):
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/payments", "customer_payments_multiple")

    customer = client.customers.get(CUSTOMER_ID)
    payments = client.payments.on(customer).list()
    assert_list_object(payments, Payment)


def test_create_customer_payment(client, response):
    """Create a customer payment."""
    response.post(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/payments", "payment_single")

    payment = client.payments.with_parent_id(CUSTOMER_ID).create(
        {
            "amount": {"currency": "EUR", "value": "10.00"},
            "description": "Order #12345",
            "redirectUrl": "https://webshop.example.org/order/12345/",
            "webhookUrl": "https://webshop.example.org/payments/webhook/",
            "method": "ideal",
        }
    )
    assert isinstance(payment, Payment)
    assert payment.customer_id == CUSTOMER_ID


def test_list_customer_payments_through_deprecated_path_raises_warning(client, response):
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/payments", "customer_payments_multiple")
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")

    with pytest.warns(
        RemovedIn215Warning,
        match=re.escape(
            "Using client.customer_payments is deprecated, use client.payments.with_parent_id(<customer_id>).list() "
            "to retrieve Customer payments."
        ),
    ):
        client.customer_payments.with_parent_id(CUSTOMER_ID).list()

    customer = client.customers.get(CUSTOMER_ID)
    with pytest.warns(
        RemovedIn215Warning,
        match=re.escape(
            "Using client.customer_payments is deprecated, use client.payments.on(<customer_object>).list() "
            "to retrieve Customer payments."
        ),
    ):
        client.customer_payments.on(customer).list()
