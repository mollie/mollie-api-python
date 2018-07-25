from mollie.api.objects.list import List
from mollie.api.objects.refund import Refund
PAYMENT_ID = 'tr_7UhSN1zuXS'
REFUND_ID = 're_4qqhO89gsT'


def test_list_all_refunds(client, response):
    """Retrieve a list of all refunds"""
    response.get('https://api.mollie.com/v2/refunds', 'refunds_multiple')
    refunds = client.refunds.all()
    assert refunds.count == 1
    assert isinstance(refunds, List)

    iterated = 0
    iterated_refund_ids = []
    for refund in refunds:
        assert isinstance(refund, Refund)
        iterated += 1
        assert refund.id is not None
        iterated_refund_ids.append(refund.id)
    assert iterated == refunds.count
    assert len(set(iterated_refund_ids)) == refunds.count


def test_list_all_refunds_of_payment(client, response):
    """Retrieve a list of all refunds of a payment"""
    response.get('https://api.mollie.com/v2/payments/%s/refunds' % PAYMENT_ID, 'refunds_multiple')
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payments_create')
    payment = client.payments.get(PAYMENT_ID)
    refunds = client.payments.refunds(payment).all()
    assert refunds.count == 1
    assert isinstance(refunds, List)

    iterated = 0
    iterated_refund_ids = []
    for refund in refunds:
        assert isinstance(refund, Refund)
        iterated += 1
        assert refund.id is not None
        iterated_refund_ids.append(refund.id)
    assert iterated == refunds.count
    assert len(set(iterated_refund_ids)) == refunds.count


def test_get_refund(client, response):
    """Retrieve a specific refund of a payment"""
    response.get('https://api.mollie.com/v2/payments/%s/refunds/%s' % (PAYMENT_ID, REFUND_ID), 'refunds_single')
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payments_create')

    payment = client.payments.get(PAYMENT_ID)
    refund = client.payments.refunds(payment).get(REFUND_ID)
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
    """Create a refund of a payment"""
    response.post('https://api.mollie.com/v2/payments/%s/refunds' % PAYMENT_ID, 'refunds_single')
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payments_create')

    payment = client.payments.get(PAYMENT_ID)
    data = {
        'amount': {'value': '5.95', 'currency': 'EUR'}
    }
    refund = client.payments.refund(payment, data)
    assert refund.id == REFUND_ID
    assert isinstance(refund, Refund)


def test_cancel_refund(client, response):
    """Cancel a refund of a payment"""
    response.get('https://api.mollie.com/v2/payments/%s/refunds/%s' % (PAYMENT_ID, REFUND_ID), 'refunds_single')
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payments_create')
    response.delete('https://api.mollie.com/v2/payments/%s/refunds/%s' % (PAYMENT_ID, REFUND_ID), 'empty')

    payment = client.payments.get(PAYMENT_ID)
    refund = client.payments.refunds(payment).get(REFUND_ID)
    canceled_refund = refund.cancel()
    assert canceled_refund == {}
    assert isinstance(refund, Refund)
