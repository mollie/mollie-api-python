import pytest

from mollie.api.error import IdentifierError
from mollie.api.objects.payment_link import PaymentLink

from .utils import assert_list_object

PAYMENT_LINK_ID = "pl_4Y0eZitmBnQ6IDoMqZQKh"


def test_list_payment_links(client, response):
    """Retrieve the list of payment links."""
    response.get("https://api.mollie.com/v2/payment-links", "payment_links_list")
    payment_links = client.payment_links.list()
    assert_list_object(payment_links, PaymentLink)


def test_create_payment_link(client, response):
    response.post("https://api.mollie.com/v2/payment-links", "payment_link_single")

    payment_link = client.payment_links.create(
        {
            "amount": {"currency": "EUR", "value": "10.00"},
            "description": "Some description",
            "redirectUrl": "https://webshop.example.org/order/12345/",
            "webhookUrl": "https://webshop.example.org/payment-links/webhook/",
            "expiresAt": "2022-12-05T18:00:00+01:00",
        }
    )
    assert payment_link.id == PAYMENT_LINK_ID


def test_get_single_payment_link(client, response):
    response.get(f"https://api.mollie.com/v2/payment-links/{PAYMENT_LINK_ID}", "payment_link_single")

    payment_link = client.payment_links.get(PAYMENT_LINK_ID)
    assert isinstance(payment_link, PaymentLink)

    # properties
    assert payment_link.resource == "payment-link"
    assert payment_link.id == PAYMENT_LINK_ID
    assert payment_link.description == "Bicycle tires"
    assert payment_link.mode == "test"
    assert payment_link.profile_id == "pfl_QkEhN94Ba"
    assert payment_link.amount == {"currency": "EUR", "value": "24.95"}
    assert payment_link.redirect_url == "https://webshop.example.org/thanks"
    assert payment_link.webhook_url == "https://webshop.example.org/payment-links/webhook/"
    assert payment_link.created_at == "2021-03-20T09:13:37+00:00"
    assert payment_link.paid_at == "2021-03-21T09:13:37+00:00"
    assert payment_link.updated_at == "2021-03-21T09:13:37+00:00"
    assert payment_link.expires_at is None
    # properties from _links
    assert payment_link.payment_link == "https://paymentlink.mollie.com/payment/4Y0eZitmBnQ6IDoMqZQKh/"
    # additional methods
    assert payment_link.is_paid() is True
    assert payment_link.has_expiration_date() is False


def test_get_payment_link_invalid_id(client):
    """Verify that an invalid payment id is validated and an error is raised."""
    with pytest.raises(IdentifierError) as excinfo:
        client.payment_links.get("invalid")
    assert str(excinfo.value) == "Invalid payment link ID 'invalid', it should start with 'pl_'."
