from mollie.api.objects.chargeback import Chargeback
from mollie.api.objects.list import List
from mollie.api.objects.refund import Refund
from mollie.api.objects.payment import Payment

PAYMENT_ID = 'tr_7UhSN1zuXS'
REFUND_ID = 're_4qqhO89gsT'
CHARGEBACK_ID = 'chb_n9z0tp'


def test_get_all_payments(client, response):
    response.get('https://api.mollie.com/v2/payments', 'payments_multiple')

    payments = client.payments.all()
    assert isinstance(payments, List)
    assert payments.count == 3
    iterated = 0
    iterated_payment_ids = []
    for payment in payments:
        iterated += 1
        assert isinstance(payment, Payment)
        assert payment.id is not None
        iterated_payment_ids.append(payment.id)
    assert iterated == payments.count, 'Unexpected amount of payments retrieved'
    assert len(set(iterated_payment_ids)) == payments.count, 'Unexpected unique payment ids retrieved'


def test_create_payment(client, response):
    """Create a new payment"""
    response.post('https://api.mollie.com/v2/payments', 'payments_create')

    payment = client.payments.create(
        {
            'amount': {'currency': 'EUR', 'value': '10.00'},
            'description': 'Order #12345',
            'redirectUrl': 'https://webshop.example.org/order/12345/',
            'webhookUrl': 'https://webshop.example.org/payments/webhook/',
            'method': 'ideal',
        })
    assert payment.id == PAYMENT_ID


def test_cancel_payment(client, response):
    """Cancel existing payment"""
    response.delete('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payments_canceled', 200)

    canceled_payment = client.payments.delete(PAYMENT_ID)
    assert canceled_payment.is_canceled() is True
    assert canceled_payment.canceled_at == '2018-03-20T09:28:37+00:00'
    assert canceled_payment.id == PAYMENT_ID


def test_get_single_payment(client, response):
    """Retrieve a single payment by payment id"""
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payments_create')

    payment = client.payments.get(PAYMENT_ID)
    assert payment.amount == {'value': '10.00', 'currency': 'EUR'}
    assert payment.description == 'Order #12345'
    assert payment.redirect_url == 'https://webshop.example.org/order/12345/'
    assert payment.webhook_url == 'https://webshop.example.org/payments/webhook/'
    assert payment.created_at == '2018-03-20T09:13:37+00:00'
    assert payment.expires_at == '2018-03-20T09:28:37+00:00'
    assert payment.profile_id == 'pfl_QkEhN94Ba'
    assert payment.method == 'ideal'
    assert payment.metadata == {'order_id': '12345'}
    assert payment.sequence_type == 'oneoff'
    assert payment.profile_id == 'pfl_QkEhN94Ba'
    assert payment.is_open() is True
    assert payment.is_pending() is False
    assert payment.is_canceled() is False
    assert payment.is_cancelable is False
    assert payment.is_expired() is False
    assert payment.is_paid() is False
    assert payment.is_failed() is False
    assert payment.has_refunds() is True
    assert payment.has_sequence_type_first() is False
    assert payment.can_be_refunded is False
    assert payment.has_sequence_type_recurring() is False
    assert payment.checkout_url == 'https://www.mollie.com/payscreen/select-method/7UhSN1zuXS'
    assert payment.resource == 'payment'
    assert payment.id == PAYMENT_ID
    assert payment.mode == 'test'
    assert payment.status == 'open'
    assert payment.get_amount_refunded == 0.0
    assert payment.get_amount_remaining == 0.0


def test_get_all_related_refunds_of_payment(client, response):
    """Retrieve a list of all refunds related to a payment"""
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payments_create')
    response.get('https://api.mollie.com/v2/payments/%s/refunds/%s' % (PAYMENT_ID, REFUND_ID), 'refunds_multiple')

    payment = client.payments.get(PAYMENT_ID)
    refunds = payment.refunds
    assert refunds.count == 1
    assert isinstance(refunds, List)

    iterated = 0
    iterated_refund_ids = []
    for refund in refunds:
        assert isinstance(refund, Refund)
        iterated += 1
        assert refund.id is not None
        iterated_refund_ids.append(refund.id)
    assert iterated == refunds.count, 'Unexpected amount of refunds retrieved'
    assert len(set(iterated_refund_ids)) == refunds.count, 'Expected unique refund ids retrieved'


def test_get_related_chargebacks(client, response):
    """Get chargebacks related to payment id"""
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payments_create')
    response.get('https://api.mollie.com/v2/payments/%s/chargebacks' % PAYMENT_ID, 'chargeback_list')

    payment = client.payments.get(PAYMENT_ID)
    chargebacks = payment.chargebacks

    assert isinstance(chargebacks, List)
    iterated = 0
    for chargeback in chargebacks:
        assert isinstance(chargeback, Chargeback)
        iterated += 1
    assert iterated == chargebacks.count
