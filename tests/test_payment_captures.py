import re

import pytest

from mollie.api.error import IdentifierError, RemovedIn215Warning
from mollie.api.objects.capture import Capture
from mollie.api.objects.payment import Payment
from mollie.api.objects.settlement import Settlement
from mollie.api.objects.shipment import Shipment
from mollie.api.resources.captures import Captures

from .utils import assert_list_object

PAYMENT_ID = "tr_7UhSN1zuXS"
CAPTURE_ID = "cpt_4qqhO89gsT"
SETTLEMENT_ID = "stl_jDk30akdN"
SHIPMENT_ID = "shp_3wmsgCJN4U"


def test_capture_resource_class(client, response):
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/captures/{CAPTURE_ID}", "capture_single")
    client.captures.with_parent_id(PAYMENT_ID).get(CAPTURE_ID)
    assert isinstance(Capture.get_resource_class(client), Captures)


def test_list_payment_captures_by_payment_id(client, response):
    """Get capture relevant to payment by payment id."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/captures", "captures_list")

    captures = client.captures.with_parent_id(PAYMENT_ID).list()
    assert_list_object(captures, Capture)


def test_get_single_payment_capture(client, response):
    """Get a single capture relevant to payment by payment id."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/captures/{CAPTURE_ID}", "capture_single")

    capture = client.captures.with_parent_id(PAYMENT_ID).get(CAPTURE_ID)
    assert isinstance(capture, Capture)
    assert capture.id == CAPTURE_ID
    assert capture.mode == "live"
    assert capture.amount == {"currency": "EUR", "value": "1027.99"}
    assert capture.settlement_amount == {"currency": "EUR", "value": "399.00"}
    assert capture.created_at == "2018-08-02T09:29:56+00:00"
    assert capture.payment_id == PAYMENT_ID
    assert capture.shipment_id == "shp_3wmsgCJN4U"
    assert capture.settlement_id == "stl_jDk30akdN"


def test_get_payment_capture_by_deprecated_parent_param_raises_warning(client, response):
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/captures/{CAPTURE_ID}", "capture_single")
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")

    with pytest.warns(RemovedIn215Warning, match="Use parameter 'parent_id' to specify a Parent ID for captures."):
        client.captures.with_parent_id(payment_id=PAYMENT_ID).get(CAPTURE_ID)

    payment = client.payments.get(PAYMENT_ID)
    with pytest.warns(RemovedIn215Warning, match="Use parameter 'parent' to specify a Parent for captures."):
        client.captures.on(payment=payment).get(CAPTURE_ID)


def test_list_payment_captures_by_payment_object(client, response):
    """Get a list of capture relevant to payment object."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/captures", "captures_list")
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    payment = client.payments.get(PAYMENT_ID)
    captures = client.captures.on(payment).list()
    assert_list_object(captures, Capture)


def test_get_single_payment_capture_by_payment_object(client, response):
    """Get a single capture relevant to payment object."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/captures/{CAPTURE_ID}", "capture_single")
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")

    payment = client.payments.get(PAYMENT_ID)
    capture = client.captures.on(payment).get(CAPTURE_ID)
    assert isinstance(capture, Capture)
    assert capture.payment_id == PAYMENT_ID


def test_capture_get_related_payment(client, response):
    """Verify the related payment of a capture."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/captures/{CAPTURE_ID}", "capture_single")
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")

    capture = client.captures.with_parent_id(PAYMENT_ID).get(CAPTURE_ID)
    payment = capture.payment
    assert isinstance(payment, Payment)
    assert payment.id == PAYMENT_ID


def test_capture_get_related_shipment(client, response):
    """Verify the related shipment of a capture."""

    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/captures/{CAPTURE_ID}", "capture_single")
    response.get("https://api.mollie.com/v2/orders/ord_8wmqcHMN4U/shipments/shp_3wmsgCJN4U", "shipment_single")

    capture = client.captures.with_parent_id(PAYMENT_ID).get(CAPTURE_ID)
    shipment = capture.shipment
    assert isinstance(shipment, Shipment)
    assert shipment.id == SHIPMENT_ID


def test_capture_get_related_settlement(client, response):
    """Verify the related settlement of a capture."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/captures/{CAPTURE_ID}", "capture_single")
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")

    capture = client.captures.with_parent_id(PAYMENT_ID).get(CAPTURE_ID)
    settlement = capture.settlement
    assert isinstance(settlement, Settlement)


def test_get_capture_without_parent_raises_error(client, response):
    with pytest.raises(IdentifierError, match=re.escape("Parent is missing, use with_parent_id() or on() to set it.")):
        client.captures.get(CAPTURE_ID)


def test_get_capture_with_invalid_parent_raises_error(client):
    with pytest.raises(
        IdentifierError, match="Invalid Parent, the parent of a Capture should be a Payment or a Settlement."
    ):
        client.captures.with_parent_id(SHIPMENT_ID).get(CAPTURE_ID)
