from mollie.api.objects.list import List
from mollie.api.objects.refund import Refund

BOOLEANS = [True, False]
PAYMENT_ID = 'tr_7UhSN1zuXS'
REFUND_ID = 're_4qqhO89gsT'


def test_payments_all(client, response):
    response.get('https://api.mollie.com/v2/payments', 'payments_multiple')

    payments = client.payments.all()
    assert payments.count == 3
    iterated = 0
    for payment in payments:
        iterated += 1
        assert payment.is_open in BOOLEANS
        assert payment.is_pending in BOOLEANS
        assert payment.is_canceled in BOOLEANS
        assert payment.is_expired in BOOLEANS
        assert payment.is_paid in BOOLEANS
        assert payment.is_failed in BOOLEANS
        assert payment.resource == "payment"
        assert payment.id is not None
        assert payment.mode == "test"
        assert payment.created_at is not None
        assert payment.amount['currency'] is not None
        assert payment.amount['value'] is not None
        assert payment.description is not None
        assert payment.method is not None
        assert payment.status is not None
        assert payment.is_cancelable in BOOLEANS
        assert payment.expires_at is not None
        assert payment.profile_id is not None
        assert payment.sequence_type is not None
        assert payment.redirect_url is not None
        assert payment.webhook_url is not None
        assert payment.settlement_amount['value'] is not None
        assert payment.settlement_amount['currency'] is not None
        assert payment.metadata['order_id'] is not None
        assert payment.checkout_url is not None
        assert payment.can_be_refunded in BOOLEANS
        assert payment.has_refunds in BOOLEANS
        assert payment.has_chargebacks in BOOLEANS
    assert iterated == 3


def test_create_payment(client, response):
    response.post('https://api.mollie.com/v2/payments', 'payments_create')
    payment = client.payments.create(
        {
            'amount': {'currency': 'EUR', 'value': '10.00'},
            'description': 'Order #12345',
            'redirectUrl': 'https://webshop.example.org/order/12345/',
            'webhookUrl': 'https://webshop.example.org/payments/webhook/',
            'method': 'ideal',
        })
    assert payment.amount['value'] == '10.00'
    assert payment.amount['currency'] == 'EUR'
    assert payment.description == 'Order #12345'
    assert payment.redirect_url == 'https://webshop.example.org/order/12345/'
    assert payment.webhook_url == 'https://webshop.example.org/payments/webhook/'
    assert payment.is_cancelable is False
    assert payment.created_at is not None
    assert payment.expires_at is not None
    assert payment.profile_id is not None
    assert payment.method == 'ideal'
    assert payment.metadata['order_id'] == '12345'
    assert payment.sequence_type == 'oneoff'
    assert payment.profile_id == 'pfl_QkEhN94Ba'
    assert payment.is_open in BOOLEANS
    assert payment.is_pending in BOOLEANS
    assert payment.is_canceled in BOOLEANS
    assert payment.is_expired in BOOLEANS
    assert payment.is_paid in BOOLEANS
    assert payment.is_failed in BOOLEANS


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
