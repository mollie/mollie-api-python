import pytest

from mollie.api.error import IdentifierError
from mollie.api.objects.capture import Capture
from mollie.api.objects.chargeback import Chargeback
from mollie.api.objects.customer import Customer
from mollie.api.objects.mandate import Mandate
from mollie.api.objects.method import Method
from mollie.api.objects.order import Order
from mollie.api.objects.payment import Payment
from mollie.api.objects.refund import Refund
from mollie.api.objects.settlement import Settlement
from mollie.api.objects.subscription import Subscription

from .utils import assert_list_object

PAYMENT_ID = "tr_7UhSN1zuXS"
REFUND_ID = "re_4qqhO89gsT"
CHARGEBACK_ID = "chb_n9z0tp"
CUSTOMER_ID = "cst_8wmqcHMN4U"
SETTLEMENT_ID = "stl_jDk30akdN"
MANDATE_ID = "mdt_h3gAaD5zP"
SUBSCRIPTION_ID = "sub_rVKGtNd6s3"
ORDER_ID = "ord_kEn1PlbGa"


def test_list_payments(client, response):
    """Retrieve a list of payments."""
    response.get("https://api.mollie.com/v2/payments", "payments_list")

    payments = client.payments.list()
    assert_list_object(payments, Payment)


def test_create_payment(client, response):
    """Create a new payment."""
    response.post("https://api.mollie.com/v2/payments", "payment_single")

    payment = client.payments.create(
        {
            "amount": {"currency": "EUR", "value": "10.00"},
            "description": "Order #12345",
            "redirectUrl": "https://webshop.example.org/order/12345/",
            "cancelUrl": "https://webshop.example.org/payment-canceled",
            "webhookUrl": "https://webshop.example.org/payments/webhook/",
            "method": "ideal",
        }
    )
    assert payment.id == PAYMENT_ID


def test_cancel_payment(client, response):
    """Cancel existing payment."""
    response.delete(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_canceled", 200)

    canceled_payment = client.payments.delete(PAYMENT_ID)
    assert isinstance(canceled_payment, Payment)
    assert canceled_payment.is_canceled() is True
    assert canceled_payment.canceled_at == "2018-03-20T09:28:37+00:00"
    assert canceled_payment.id == PAYMENT_ID


def test_cancel_payment_invalid_id(client):
    """Verify that an invalid payment id is validated and an error is raised."""
    with pytest.raises(IdentifierError) as excinfo:
        client.payments.delete("invalid")
    assert str(excinfo.value) == "Invalid payment ID 'invalid', it should start with 'tr_'."


def test_get_single_payment(client, response):
    """Retrieve a single payment by payment id."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single_no_links")

    payment = client.payments.get(PAYMENT_ID)
    assert isinstance(payment, Payment)
    # properties
    assert payment.resource == "payment"
    assert payment.id == PAYMENT_ID
    assert payment.mode == "test"
    assert payment.created_at == "2018-03-20T09:13:37+00:00"
    assert payment.status == Payment.STATUS_OPEN
    assert payment.is_cancelable is False
    assert payment.paid_at is None
    assert payment.canceled_at is None
    assert payment.authorized_at is None
    assert payment.expires_at == "2018-03-20T09:28:37+00:00"
    assert payment.expired_at is None
    assert payment.failed_at is None
    assert payment.amount == {"value": "10.00", "currency": "EUR"}
    assert payment.amount_refunded is None
    assert payment.amount_remaining is None
    assert payment.amount_captured == {"currency": "EUR", "value": "1.00"}
    assert payment.amount_chargedback == {"value": "5.00", "currency": "EUR"}
    assert payment.description == "Order #12345"
    assert payment.redirect_url == "https://webshop.example.org/order/12345/"
    assert payment.webhook_url == "https://webshop.example.org/payments/webhook/"
    assert payment.cancel_url == "https://webshop.example.org/payment-canceled"
    assert payment.method == Method.IDEAL
    assert payment.metadata == {"order_id": "12345"}
    assert payment.locale is None
    assert payment.country_code is None
    assert payment.profile_id == "pfl_QkEhN94Ba"
    assert payment.customer_id == CUSTOMER_ID
    assert payment.sequence_type == Payment.SEQUENCETYPE_RECURRING
    assert payment.application_fee is None
    assert payment.details is None
    assert payment.routing is not None
    assert payment.subscription_id is None
    assert payment.settlement_id is None
    assert payment.capture_mode == "automatic"
    assert payment.capture_before == "2023-01-20T09:13:37+00+00"
    assert payment.capture_delay == "20 hours"
    # properties from _links
    assert payment.checkout_url == "https://www.mollie.com/payscreen/select-method/7UhSN1zuXS"
    assert payment.changepaymentstate_url is None
    assert payment.payonline_url is None
    assert payment.refunds is not None
    assert payment.chargebacks is not None
    assert payment.captures is not None
    # additional methods
    assert payment.is_open() is True
    assert payment.is_pending() is False
    assert payment.is_canceled() is False
    assert payment.is_expired() is False
    assert payment.is_paid() is False
    assert payment.is_failed() is False
    assert payment.is_authorized() is False
    assert payment.has_refunds() is False
    assert payment.has_chargebacks() is False
    assert payment.has_captures() is False
    assert payment.has_settlement() is False
    assert payment.has_split_payments() is True
    assert payment.can_be_refunded() is False
    assert payment.has_sequence_type_first() is False
    assert payment.has_sequence_type_recurring() is True


def test_get_payment_invalid_id(client):
    with pytest.raises(IdentifierError) as excinfo:
        client.payments.get("invalid")
    assert str(excinfo.value) == "Invalid payment ID 'invalid', it should start with 'tr_'."


def test_payment_get_related_refunds(client, response):
    """Retrieve a list of refunds related to a payment."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/refunds", "refunds_list")

    payment = client.payments.get(PAYMENT_ID)
    refunds = payment.refunds.list()
    assert_list_object(refunds, Refund)


def test_payment_get_related_chargebacks(client, response):
    """Get chargebacks related to payment id."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/chargebacks", "chargebacks_list")

    payment = client.payments.get(PAYMENT_ID)
    chargebacks = payment.chargebacks.list()
    assert_list_object(chargebacks, Chargeback)


def test_payment_get_related_captures(client, response):
    """Get captures related to payment."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/captures", "captures_list")

    payment = client.payments.get(PAYMENT_ID)
    captures = payment.captures.list()
    assert_list_object(captures, Capture)


def test_payment_get_related_settlement(client, response):
    """Get the settlement related to the payment."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")

    payment = client.payments.get(PAYMENT_ID)
    assert payment.settlement_id == SETTLEMENT_ID
    assert payment.settlement_amount == {"currency": "EUR", "value": "39.75"}

    settlement = payment.get_settlement()
    assert isinstance(settlement, Settlement)
    assert settlement.id == SETTLEMENT_ID


def test_payment_get_related_mandate(client, response):
    """Get the mandate related to the payment."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/mandates/{MANDATE_ID}", "customer_mandate_single")

    payment = client.payments.get(PAYMENT_ID)
    mandate = payment.get_mandate()
    assert isinstance(mandate, Mandate)
    assert mandate.id == MANDATE_ID


def test_payment_get_related_subscription(client, response):
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}", "subscription_single"
    )

    payment = client.payments.get(PAYMENT_ID)
    subscription = payment.get_subscription()
    assert isinstance(subscription, Subscription)
    assert subscription.id == SUBSCRIPTION_ID


def test_payment_get_related_customer(client, response):
    """Get customer related to payment."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")

    payment = client.payments.get(PAYMENT_ID)
    customer = payment.get_customer()
    assert isinstance(customer, Customer)
    assert customer.id == CUSTOMER_ID


def test_payment_get_related_order(client, response):
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_single")

    payment = client.payments.get(PAYMENT_ID)
    order = payment.get_order()
    assert isinstance(order, Order)
    assert order.id == ORDER_ID


def test_update_payment(client, response):
    """Update an existing payment."""
    response.patch(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_updated")

    data = {
        "description": "Order #12346",
        "redirectUrl": "https://webshop.example.org/order/12346/",
        "webhookUrl": "https://webshop.example.org/payments/webhook/",
        "metadata": {"order_id": "12346"},
    }
    updated_payment = client.payments.update(PAYMENT_ID, data)
    assert isinstance(updated_payment, Payment)
    assert updated_payment.description == "Order #12346"


def test_update_payment_invalid_id(client):
    data = {}
    with pytest.raises(IdentifierError) as excinfo:
        client.payments.update("invalid", data)
    assert str(excinfo.value) == "Invalid payment ID 'invalid', it should start with 'tr_'."
