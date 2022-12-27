import pytest

from mollie.api.error import IdentifierError
from mollie.api.objects.order import Order
from mollie.api.objects.order_line import OrderLine
from mollie.api.objects.payment import Payment
from mollie.api.objects.refund import Refund
from mollie.api.objects.settlement import Settlement

from .utils import assert_list_object

PAYMENT_ID = "tr_7UhSN1zuXS"
REFUND_ID = "re_4qqhO89gsT"
ORDER_ID = "ord_kEn1PlbGa"
SETTLEMENT_ID = "stl_jDk30akdN"


@pytest.fixture
def payment(client, response):
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    return client.payments.get(PAYMENT_ID)


@pytest.fixture
def refund(payment, response):
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/refunds/{REFUND_ID}", "refund_single")
    return payment.refunds.get(REFUND_ID)


def test_get_payment_refund(client, response):
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/refunds/{REFUND_ID}", "refund_single_no_links")

    payment = client.payments.get(PAYMENT_ID)
    refund = payment.refunds.get(REFUND_ID)
    assert isinstance(refund, Refund)
    # properties
    assert refund.resource == "refund"
    assert refund.id == REFUND_ID
    assert refund.amount == {"currency": "EUR", "value": "5.95"}
    assert refund.settlement_id is None
    assert refund.settlement_amount is None
    assert refund.description == "Required quantity not in stock, refunding one photo book."
    assert refund.metadata == {"bookkeeping_id": 12345}
    assert refund.status == Refund.STATUS_PENDING
    assert_list_object(refund.lines, OrderLine)
    assert refund.payment_id == PAYMENT_ID
    assert refund.order_id is None
    assert refund.created_at == "2018-03-14T17:09:02.0Z"
    # additional methods
    assert refund.is_queued() is False
    assert refund.is_pending() is True
    assert refund.is_processing() is False
    assert refund.is_refunded() is False


def test_get_payment_refund_invalid_id(client, response):
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")

    payment = client.payments.get(PAYMENT_ID)
    with pytest.raises(IdentifierError) as excinfo:
        payment.refunds.get("invalid")
    assert str(excinfo.value) == "Invalid Refund ID 'invalid', it should start with 're_'."


def test_payment_refund_get_related_payment(refund, response):
    """Verify the related payment of a refund."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")

    assert refund.payment_id == PAYMENT_ID
    payment = refund.get_payment()
    assert isinstance(payment, Payment)
    assert payment.id == PAYMENT_ID


def test_payment_refund_get_related_settlement(refund, response):
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")

    assert refund.settlement_id == SETTLEMENT_ID
    assert refund.settlement_amount == {"currency": "EUR", "value": "10.00"}
    settlement = refund.get_settlement()
    assert isinstance(settlement, Settlement)
    assert settlement.id == SETTLEMENT_ID


def test_payment_refund_get_related_order(refund, response):
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_single")

    assert refund.order_id == ORDER_ID
    order = refund.get_order()
    assert isinstance(order, Order)
    assert order.id == ORDER_ID


def test_create_payment_refund(payment, response):
    """Create a payment refund of a payment."""
    response.post(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/refunds", "refund_single")

    data = {"amount": {"value": "5.95", "currency": "EUR"}}
    refund = payment.refunds.create(data)
    assert isinstance(refund, Refund)
    assert refund.id == REFUND_ID


def test_cancel_payment_refund(payment, response):
    """Cancel a refund of a payment."""
    response.delete(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/refunds/{REFUND_ID}", "empty")

    canceled_refund = payment.refunds.delete(REFUND_ID)
    assert canceled_refund == {}
