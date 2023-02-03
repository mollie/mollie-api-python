import json

import pytest
from responses import matchers

from mollie.api.error import EmbedNotFound, IdentifierError
from mollie.api.objects.order import Order
from mollie.api.objects.payment import Payment
from mollie.api.objects.refund import Refund
from mollie.api.resources import OrderPayments, OrderRefunds, OrderShipments

from .utils import assert_list_object

ORDER_ID = "ord_kEn1PlbGa"


def test_get_order(client, response):
    """Retrieve a single order by order ID."""
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_single")

    order = client.orders.get(ORDER_ID)
    assert isinstance(order, Order)
    assert order.id == "ord_kEn1PlbGa"
    assert order.resource == "order"
    assert order.profile_id == "pfl_URR55HPMGx"
    assert order.method == "ideal"
    assert order.mode == "live"
    assert order.amount == {"value": "1027.99", "currency": "EUR"}
    assert order.amount_captured is None
    assert order.amount_refunded is None
    assert order.status == "created"
    assert order.is_cancelable is True
    assert order.billing_address == {
        "streetAndNumber": "Keizersgracht 313",
        "city": "Amsterdam",
        "region": "Noord-Holland",
        "postalCode": "1234AB",
        "country": "NL",
        "title": "Dhr.",
        "givenName": "Piet",
        "familyName": "Mondriaan",
        "email": "piet@mondriaan.com",
        "phone": "+31309202070",
    }
    assert order.consumer_date_of_birth == "1958-01-31"
    assert order.order_number == "1337"
    assert order.shipping_address == {
        "streetAndNumber": "Keizersgracht 313",
        "streetAdditional": "4th floor",
        "city": "Haarlem",
        "region": "Noord-Holland",
        "postalCode": "5678AB",
        "country": "NL",
        "title": "Mr.",
        "givenName": "Chuck",
        "familyName": "Norris",
        "email": "norris@chucknorrisfacts.net",
    }
    assert order.locale == "nl_NL"
    assert order.metadata == {"description": "Lego cars", "order_id": "1337"}
    assert order.redirect_url == "https://example.org/redirect"
    assert order.cancel_url == "https://example.org/payment-canceled"
    assert order.webhook_url == "https://example.org/webhook"
    assert order.created_at == "2018-08-02T09:29:56+00:00"
    assert order.expires_at == "2018-08-30T09:29:56+00:00"
    assert order.expired_at is None
    assert order.paid_at is None
    assert order.authorized_at is None
    assert order.canceled_at is None
    assert order.completed_at is None
    assert order.checkout_url == "https://www.mollie.com/payscreen/order/checkout/kEn1PlbGa"
    assert isinstance(order.shipments, OrderShipments)
    assert isinstance(order.refunds, OrderRefunds)
    assert isinstance(order.payments, OrderPayments)

    assert order.is_created() is True
    assert order.is_paid() is False
    assert order.is_authorized() is False
    assert order.is_shipping() is False
    assert order.is_completed() is False
    assert order.is_expired() is False


def test_get_order_invalid_id(client):
    with pytest.raises(IdentifierError) as excinfo:
        client.orders.get("invalid")
    assert str(excinfo.value) == "Invalid order ID 'invalid', it should start with 'ord_'."


def test_list_orders(client, response):
    """Retrieve a list of existing orders."""
    response.get("https://api.mollie.com/v2/orders", "orders_list")

    orders = client.orders.list()
    assert_list_object(orders, Order)


def test_create_order_refund(client, response):
    """Create an order refund of an order."""
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_single")
    response.post(f"https://api.mollie.com/v2/orders/{ORDER_ID}/refunds", "refund_single")

    data = {
        "lines": [
            {
                "id": "odl_dgtxyl",
                "quantity": 1,
            }
        ],
        "description": "Required quantity not in stock, refunding one photo book.",
        "metadata": {
            "bookkeeping_id": 12345,
        },
    }

    order = client.orders.get(ORDER_ID)
    refund = order.refunds.create(data)
    assert isinstance(refund, Refund)
    assert refund.status == Refund.STATUS_PENDING
    assert refund.description == "Required quantity not in stock, refunding one photo book."
    assert refund.metadata == {"bookkeeping_id": 12345}


def test_create_order_refund_all_lines(client, response):
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_single")
    response.post(f"https://api.mollie.com/v2/orders/{ORDER_ID}/refunds", "refund_single")

    order = client.orders.get(ORDER_ID)
    refund = order.refunds.create()
    assert isinstance(refund, Refund)

    # Inspect the request that was made
    request = response.calls[-1].request
    assert request.url == f"https://api.mollie.com/v2/orders/{ORDER_ID}/refunds"
    assert json.loads(request.body) == {
        "lines": []
    }, "An empty list of lines should be generated, so all lines will be refunded."


def test_create_order(client, response):
    """Create an order."""
    response.post("https://api.mollie.com/v2/orders", "order_single")

    data = {
        "amount": {"value": "1027.99", "currency": "EUR"},
        "billingAddress": {
            "streetAndNumber": "Keizersgracht 313",
            "city": "Amsterdam",
            "region": "Noord-Holland",
            "postalCode": "1234AB",
            "country": "NL",
            "givenName": "Piet",
            "familyName": "Mondriaan",
            "email": "piet@mondriaan.com",
        },
        "shippingAddress": {
            "streetAndNumber": "Prinsengracht 313",
            "city": "Haarlem",
            "region": "Noord-Holland",
            "postalCode": "5678AB",
            "country": "NL",
            "givenName": "Chuck",
            "familyName": "Norris",
            "email": "norris@chucknorrisfacts.net",
        },
        "metadata": {"order_id": "1337", "description": "Lego cars"},
        "consumerDateOfBirth": "1958-01-31",
        "locale": "nl_NL",
        "orderNumber": "1337",
        "redirectUrl": "https://example.org/redirect",
        "cancelUrl": "https://example.org/payment-canceled",
        "webhookUrl": "https://example.org/webhook",
        "method": "klarnapaylater",
        "lines": [
            {
                "type": "physical",
                "sku": "5702016116977",
                "name": "LEGO 42083 Bugatti Chiron",
                "productUrl": "https://shop.lego.com/nl-NL/Bugatti-Chiron-42083",
                "imageUrl": "https://sh-s7-live-s.legocdn.com/is/image//LEGO/42083_alt1?$main$",
                "quantity": 1,
                "vatRate": "21.00",
                "unitPrice": {"currency": "EUR", "value": "399.00"},
                "totalAmount": {"currency": "EUR", "value": "698.00"},
                "discountAmount": {"currency": "EUR", "value": "100.00"},
                "vatAmount": {"currency": "EUR", "value": "121.14"},
            },
        ],
    }
    order = client.orders.create(data)
    assert isinstance(order, Order)
    assert order.id == ORDER_ID


def test_update_order(client, response):
    """Update an existing order."""
    response.patch(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_updated")

    data = {
        "billingAddress": {
            "streetAndNumber": "Keizersgracht 313",
            "city": "Amsterdam",
            "region": "Noord-Holland",
            "postalCode": "1234AB",
            "country": "NL",
            "title": "Dhr",
            "givenName": "Piet",
            "familyName": "Mondriaan",
            "email": "piet@mondriaan.com",
            "phone": "+31208202070",
        }
    }
    updated_order = client.orders.update(ORDER_ID, data)
    assert isinstance(updated_order, Order)
    assert updated_order.billing_address["givenName"] == "Piet"


def test_update_order_invalid_id(client):
    data = {
        "billingAddress": {
            "streetAndNumber": "Keizersgracht 313",
            "city": "Amsterdam",
            "region": "Noord-Holland",
            "postalCode": "1234AB",
            "country": "NL",
            "title": "Dhr",
            "givenName": "Piet",
            "familyName": "Mondriaan",
            "email": "piet@mondriaan.com",
            "phone": "+31208202070",
        }
    }

    with pytest.raises(IdentifierError) as excinfo:
        client.orders.update("invalid", data)
    assert str(excinfo.value) == "Invalid order ID 'invalid', it should start with 'ord_'."


def test_cancel_order(client, response):
    """Cancel an existing order."""
    response.delete(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_canceled", 200)

    canceled_order = client.orders.delete(ORDER_ID)
    assert isinstance(canceled_order, Order)
    assert canceled_order.is_canceled() is True
    assert canceled_order.is_cancelable is False


def test_cancel_order_invalid_id(client):
    with pytest.raises(IdentifierError) as excinfo:
        client.orders.delete("invalid")
    assert str(excinfo.value) == "Invalid order ID 'invalid', it should start with 'ord_'."


def test_create_order_payment(client, response):
    """Create a payment for an order."""
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_single")
    response.post(f"https://api.mollie.com/v2/orders/{ORDER_ID}/payments", "payment_single")

    order = client.orders.get(ORDER_ID)
    data = {"method": "ideal"}
    payment = order.payments.create(data)
    assert isinstance(payment, Payment)
    assert payment.order_id == ORDER_ID


def test_list_embedded_payments_in_order(client, response):
    response.get(
        f"https://api.mollie.com/v2/orders/{ORDER_ID}",
        "order_single_with_embeds",
        match=[matchers.query_param_matcher({"embed": "payments"})],
    )

    order = client.orders.get(ORDER_ID, embed="payments")
    assert_list_object(order.payments.list(), Payment)


def test_list_embedded_payments_in_order_raises_error(client, response):
    """If the data is not embedded, an error is raised."""
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_single")

    order = client.orders.get(ORDER_ID)
    with pytest.raises(EmbedNotFound) as excinfo:
        order.payments.list()
    assert (
        str(excinfo.value)
        == "You tried to access embedded data, but did not request to embed 'payments' in the request."
    )
