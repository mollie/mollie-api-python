from mollie.api.objects.chargeback import Chargeback

from .utils import assert_list_object

PAYMENT_ID = 'tr_7UhSN1zuXS'
CHARGEBACK_ID = 'chb_n9z0tp'


def test_get_payment_chargebacks_by_payment_id(client, response):
    """Get chargebacks relevant to payment by payment id."""
    response.get('https://api.mollie.com/v2/payments/%s/chargebacks' % PAYMENT_ID, 'chargebacks_list')

    chargebacks = client.payment_chargebacks.with_parent_id(PAYMENT_ID).list()
    assert_list_object(chargebacks, Chargeback)


def test_get_single_payment_chargeback(client, response):
    """Get a single chargeback relevant to payment by payment id."""
    response.get('https://api.mollie.com/v2/payments/%s/chargebacks/%s' % (PAYMENT_ID, CHARGEBACK_ID),
                 'chargeback_single')

    chargeback = client.payment_chargebacks.with_parent_id(PAYMENT_ID).get(CHARGEBACK_ID)
    assert isinstance(chargeback, Chargeback)
    assert chargeback.id == CHARGEBACK_ID
    assert chargeback.amount == {'currency': 'USD', 'value': '43.38'}
    assert chargeback.settlement_amount == {'currency': 'EUR', 'value': '-35.07'}
    assert chargeback.created_at == '2018-03-14T17:00:52.0Z'
    assert chargeback.reversed_at == '2018-03-14T17:00:55.0Z'
    assert chargeback.payment_id == PAYMENT_ID


def test_list_payment_chargebacks_by_payment_object(client, response):
    """Get a list of chargebacks relevant to payment object."""
    response.get('https://api.mollie.com/v2/payments/%s/chargebacks' % PAYMENT_ID, 'chargebacks_list')
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payment_single')

    payment = client.payments.get(PAYMENT_ID)
    chargebacks = client.payment_chargebacks.on(payment).list()
    assert_list_object(chargebacks, Chargeback)


def test_get_single_payment_chargeback_by_payment_object(client, response):
    """Get a single chargeback relevant to payment object."""
    response.get('https://api.mollie.com/v2/payments/%s/chargebacks/%s' % (PAYMENT_ID, CHARGEBACK_ID),
                 'chargeback_single')
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payment_single')

    payment = client.payments.get(PAYMENT_ID)
    chargeback = client.payment_chargebacks.on(payment).get(CHARGEBACK_ID)
    assert isinstance(chargeback, Chargeback)
    assert chargeback.payment_id == PAYMENT_ID
