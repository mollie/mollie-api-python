from mollie.api.objects.chargeback import Chargeback
from mollie.api.objects.payment import Payment
from mollie.api.objects.settlement import Settlement

from .utils import assert_list_object

PAYMENT_ID = "tr_7UhSN1zuXS"
CHARGEBACK_ID = "chb_n9z0tp"
SETTLEMENT_ID = "stl_jDk30akdN"


def test_get_payment_chargebacks_by_payment_id(client, response):
    """Get chargebacks relevant to payment by payment id."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/chargebacks", "chargebacks_list")

    chargebacks = client.payment_chargebacks.with_parent_id(PAYMENT_ID).list()
    assert_list_object(chargebacks, Chargeback)


def test_get_single_payment_chargeback(client, response):
    """Get a single chargeback relevant to payment by payment id."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/chargebacks/{CHARGEBACK_ID}", "chargeback_single")
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")

    chargeback = client.payment_chargebacks.with_parent_id(PAYMENT_ID).get(CHARGEBACK_ID)
    assert isinstance(chargeback, Chargeback)
    assert chargeback.id == CHARGEBACK_ID
    assert chargeback.amount == {"currency": "USD", "value": "43.38"}
    assert chargeback.settlement_amount == {"currency": "EUR", "value": "-35.07"}
    assert chargeback.created_at == "2018-03-14T17:00:52.0Z"
    assert chargeback.reason is None
    assert chargeback.reversed_at == "2018-03-14T17:00:55.0Z"
    assert chargeback.payment_id == PAYMENT_ID
    assert isinstance(chargeback.payment, Payment)
    assert isinstance(chargeback.settlement, Settlement)


def test_list_payment_chargebacks_by_payment_object(client, response):
    """Get a list of chargebacks relevant to payment object."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/chargebacks", "chargebacks_list")
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")

    payment = client.payments.get(PAYMENT_ID)
    chargebacks = client.payment_chargebacks.on(payment).list()
    assert_list_object(chargebacks, Chargeback)


def test_get_single_payment_chargeback_by_payment_object(client, response):
    """Get a single chargeback relevant to payment object."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/chargebacks/{CHARGEBACK_ID}", "chargeback_single")
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")

    payment = client.payments.get(PAYMENT_ID)
    chargeback = client.payment_chargebacks.on(payment).get(CHARGEBACK_ID)
    assert isinstance(chargeback, Chargeback)
    assert chargeback.payment_id == PAYMENT_ID
