from mollie.api.objects.list import List
from mollie.api.objects.refund import Refund

PAYMENT_ID = 'tr_7UhSN1zuXS'
REFUND_ID = 're_4qqhO89gsT'


def test_get_refund(client, response):
    """Retrieve a specific refund of a payment."""
    response.get('https://api.mollie.com/v2/payments/%s/refunds/%s' % (PAYMENT_ID, REFUND_ID), 'refund_single')

    refund = client.payment_refunds.with_parent_id(PAYMENT_ID).get(REFUND_ID)
    assert refund.resource == 'refund'
    assert refund.id == REFUND_ID
    assert refund.amount['currency'] == 'EUR'
    assert refund.amount['value'] == '5.95'
    assert refund.settlement_amount['currency'] == 'EUR'
    assert refund.settlement_amount['value'] == '10.00'
    assert refund.description == 'Order'
    assert refund.status == 'pending'
    assert refund.created_at == '2018-03-14T17:09:02.0Z'
    assert refund.payment_id == PAYMENT_ID


def test_create_refund(client, response):
    """Create a payment refund of a payment."""
    response.post('https://api.mollie.com/v2/payments/%s/refunds' % PAYMENT_ID, 'refund_single')

    data = {
        'amount': {'value': '5.95', 'currency': 'EUR'}
    }
    refund = client.payment_refunds.with_parent_id(PAYMENT_ID).create(data)
    assert refund.id == REFUND_ID
    assert isinstance(refund, Refund)


def test_get_single_refund_on_payment_object(client, response):
    """Retrieve a payment refund of a payment."""
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payment_single')
    response.get('https://api.mollie.com/v2/payments/%s/refunds/%s' % (PAYMENT_ID, REFUND_ID), 'refund_single')

    payment = client.payments.get(PAYMENT_ID)
    refund = client.payment_refunds.on(payment).get(REFUND_ID)
    assert refund.id == REFUND_ID
    assert isinstance(refund, Refund)


def test_get_all_refunds_on_payment_object(client, response):
    """Retrieve all payment refunds of a payment."""
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payment_single')
    response.get('https://api.mollie.com/v2/payments/%s/refunds' % PAYMENT_ID, 'refunds_list')

    payment = client.payments.get(PAYMENT_ID)
    refunds = client.payment_refunds.on(payment).all()
    assert refunds.count == 1
    assert isinstance(refunds, List)

    iterated = 0
    iterated_refund_ids = []
    for refund in refunds:
        assert isinstance(refund, Refund)
        assert refund.id is not None
        iterated += 1
        iterated_refund_ids.append(refund.id)
    assert iterated == refunds.count, 'Unexpected amount of refunds retrieved'
    assert len(set(iterated_refund_ids)) == refunds.count, 'Unexpected amount of unique refund ids retrieved'


def test_cancel_refund(client, response):
    """Cancel a refund of a payment."""
    response.delete('https://api.mollie.com/v2/payments/%s/refunds/%s' % (PAYMENT_ID, REFUND_ID), 'empty')

    canceled_refund = client.payment_refunds.with_parent_id(PAYMENT_ID).delete(REFUND_ID)
    assert canceled_refund == {}
