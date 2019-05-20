from mollie.api.objects.capture import Capture

from .utils import assert_list_object

PAYMENT_ID = 'tr_7UhSN1zuXS'
CAPTURE_ID = 'cpt_4qqhO89gsT'


def test_get_payment_captures_by_payment_id(client, response):
    """Get chargebacks relevant to payment by payment id."""
    response.get('https://api.mollie.com/v2/payments/%s/captures' % PAYMENT_ID, 'captures_list')

    captures = client.captures.with_parent_id(PAYMENT_ID).list()
    assert_list_object(captures, Capture)


def test_get_single_payment_capture(client, response):
    """Get a single chargeback relevant to payment by payment id."""
    response.get('https://api.mollie.com/v2/payments/%s/captures/%s' % (PAYMENT_ID, CAPTURE_ID),
                 'capture_single')

    capture = client.captures.with_parent_id(PAYMENT_ID).get(CAPTURE_ID)
    assert isinstance(capture, Capture)
    assert capture.id == CAPTURE_ID
    assert capture.amount == {'currency': 'EUR', 'value': '1027.99'}
    assert capture.settlement_amount == {'currency': 'EUR', 'value': '399.00'}
    assert capture.created_at == '2018-08-02T09:29:56+00:00'
    assert capture.payment_id == PAYMENT_ID


def test_list_payment_captures_by_payment_object(client, response):
    """Get a list of chargebacks relevant to payment object."""
    response.get('https://api.mollie.com/v2/payments/%s/captures' % PAYMENT_ID, 'captures_list')
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payment_single')
    payment = client.payments.get(PAYMENT_ID)
    captures = client.captures.on(payment).list()
    assert_list_object(captures, Capture)


def test_get_single_payment_chargeback_by_payment_object(client, response):
    """Get a single chargeback relevant to payment object."""
    response.get('https://api.mollie.com/v2/payments/%s/captures/%s' % (PAYMENT_ID, CAPTURE_ID),
                 'chargeback_single')
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payment_single')

    payment = client.payments.get(PAYMENT_ID)
    capture = client.captures.on(payment).get(CAPTURE_ID)
    assert isinstance(capture, Capture)
    assert capture.payment_id == PAYMENT_ID
