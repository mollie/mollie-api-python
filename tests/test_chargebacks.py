from mollie.api.objects.chargeback import Chargeback
from mollie.api.objects.list import List

PAYMENT_ID = 'tr_7UhSN1zuXS'
CHARGEBACK_ID = 'chb_n9z0tp'


def test_get_chargeback_by_payment(client, response):
    response.get('https://api.mollie.com/v2/payments/%s/chargebacks' % PAYMENT_ID, 'chargeback_list')

    chargebacks = client.payment_chargebacks.with_parent_id(PAYMENT_ID).all()
    assert chargebacks.count == 1
    assert isinstance(chargebacks, List)

    iterated = 0
    iterated_chargeback_ids = []
    for chargeback in chargebacks:
        assert chargeback.id is not None
        assert isinstance(chargeback, Chargeback)
        iterated += 1
        iterated_chargeback_ids.append(chargeback.id)
    assert iterated == chargebacks.count, 'Unexpected amount of chargebacks retrieved'
    assert len(
        set(iterated_chargeback_ids)) == chargebacks.count, 'Unexpected amount of unique chargeback ids retrieved'


def test_get_single_chargeback(client, response):
    response.get('https://api.mollie.com/v2/payments/%s/chargebacks/%s' % (PAYMENT_ID, CHARGEBACK_ID),
                 'chargeback_single')

    chargeback = client.payment_chargebacks.with_parent_id(PAYMENT_ID).get(CHARGEBACK_ID)
    assert isinstance(chargeback, Chargeback)
    assert chargeback.id == CHARGEBACK_ID
    assert chargeback.amount['currency'] == 'USD'
    assert chargeback.amount['value'] == '43.38'
    assert chargeback.settlement_amount['currency'] == 'EUR'
    assert chargeback.settlement_amount['value'] == '-35.07'
    assert chargeback.created_at == '2018-03-14T17:00:52.0Z'
    assert chargeback.reversed_at == '2018-03-14T17:00:55.0Z'
    assert chargeback.payment_id == PAYMENT_ID


def test_get_all_chargebacks(client, response):
    response.get('https://api.mollie.com/v2/chargebacks', 'chargeback_list')

    chargebacks = client.chargebacks.all()
    assert chargebacks.count == 1
    assert isinstance(chargebacks, List)

    iterated = 0
    iterated_chargeback_ids = []
    for chargeback in chargebacks:
        assert chargeback.id is not None
        assert isinstance(chargeback, Chargeback)
        iterated += 1
        iterated_chargeback_ids.append(chargeback.id)
    assert iterated == chargebacks.count, 'Unexpected amount of chargebacks retrieved'
    assert len(
        set(iterated_chargeback_ids)) == chargebacks.count, 'Unexpected amount of unique chargeback ids retrieved'


def test_get_all_chargebacks_on_payment_object(client, response):
    response.get('https://api.mollie.com/v2/payments/%s/chargebacks' % PAYMENT_ID, 'chargeback_list')
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payments_create')

    payment = client.payments.get(PAYMENT_ID)
    chargebacks = client.payment_chargebacks.on(payment).all()
    assert chargebacks.count == 1
    assert isinstance(chargebacks, List)

    iterated = 0
    iterated_chargeback_ids = []
    for chargeback in chargebacks:
        assert chargeback.id is not None
        assert isinstance(chargeback, Chargeback)
        iterated += 1
        iterated_chargeback_ids.append(chargeback.id)
    assert iterated == chargebacks.count, 'Unexpected amount of chargebacks retrieved'
    assert len(
        set(iterated_chargeback_ids)) == chargebacks.count, 'Unexpected amount of unique chargeback ids retrieved'


def test_get_one_chargeback_on_payment_object(client, response):
    response.get('https://api.mollie.com/v2/payments/%s/chargebacks/%s' % (PAYMENT_ID, CHARGEBACK_ID),
                 'chargeback_single')
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payments_create')

    payment = client.payments.get(PAYMENT_ID)
    chargeback = client.payment_chargebacks.on(payment).get(CHARGEBACK_ID)
    assert chargeback.payment_id == PAYMENT_ID
    assert isinstance(chargeback, Chargeback)
