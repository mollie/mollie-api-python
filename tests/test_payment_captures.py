import pytest

from mollie.api.error import IdentifierError
from mollie.api.objects.capture import Capture
from mollie.api.objects.payment import Payment
from mollie.api.objects.settlement import Settlement
from mollie.api.objects.shipment import Shipment

from .utils import assert_list_object

PAYMENT_ID = "tr_7UhSN1zuXS"
CAPTURE_ID = "cpt_4qqhO89gsT"
SETTLEMENT_ID = "stl_jDk30akdN"
SHIPMENT_ID = "shp_3wmsgCJN4U"


def test_list_payment_captures(client, response):
    """Get capture relevant to payment by payment id."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/captures", "captures_list")

    payment = client.payments.get(PAYMENT_ID)
    captures = payment.captures.list()
    assert_list_object(captures, Capture)


def test_get_payment_capture_invalid_id(client, response):
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")

    payment = client.payments.get(PAYMENT_ID)
    with pytest.raises(IdentifierError) as excinfo:
        payment.captures.get("invalid")
    assert str(excinfo.value) == "Invalid capture ID 'invalid', it should start with 'cpt_'."


def test_get_single_payment_capture(client, response):
    """Get a single capture relevant to payment by payment id."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/captures/{CAPTURE_ID}", "capture_single")

    payment = client.payments.get(PAYMENT_ID)
    capture = payment.captures.get(CAPTURE_ID)
    assert isinstance(capture, Capture)
    assert capture.id == CAPTURE_ID
    assert capture.mode == "live"
    assert capture.amount == {"currency": "EUR", "value": "1027.99"}
    assert capture.settlement_amount == {"currency": "EUR", "value": "399.00"}
    assert capture.created_at == "2018-08-02T09:29:56+00:00"
    assert capture.payment_id == PAYMENT_ID
    assert capture.shipment_id == "shp_3wmsgCJN4U"
    assert capture.settlement_id == "stl_jDk30akdN"


def test_capture_get_related_payment(client, response):
    """Verify the related payment of a capture."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/captures/{CAPTURE_ID}", "capture_single")

    payment = client.payments.get(PAYMENT_ID)
    capture = payment.captures.get(CAPTURE_ID)
    payment = capture.get_payment()
    assert isinstance(payment, Payment)
    assert payment.id == PAYMENT_ID


def test_capture_get_related_shipment(client, response):
    """Verify the related shipment of a capture."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/captures/{CAPTURE_ID}", "capture_single")
    response.get("https://api.mollie.com/v2/orders/ord_8wmqcHMN4U/shipments/shp_3wmsgCJN4U", "shipment_single")

    payment = client.payments.get(PAYMENT_ID)
    capture = payment.captures.get(CAPTURE_ID)
    shipment = capture.get_shipment()
    assert isinstance(shipment, Shipment)
    assert shipment.id == SHIPMENT_ID


def test_capture_get_related_settlement(client, response):
    """Verify the related settlement of a capture."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/captures/{CAPTURE_ID}", "capture_single")
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")

    payment = client.payments.get(PAYMENT_ID)
    capture = payment.captures.get(CAPTURE_ID)
    settlement = capture.get_settlement()
    assert isinstance(settlement, Settlement)


def test_create_capture_for_payment(client, response):
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.post(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/captures", "capture_single")
    payment = client.payments.get(PAYMENT_ID)

    data = {"amount": {"currency": "EUR", "value": "10.00"}, "description": "Capture for order #12345"}

    capture = payment.captures.create(data)
    assert capture.id == CAPTURE_ID
