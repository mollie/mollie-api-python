from mollie.api.objects.order import Order
from mollie.api.objects.order_line import OrderLine
from mollie.api.objects.payment import Payment
from mollie.api.objects.refund import Refund

from .utils import assert_list_object

PAYMENT_ID = 'tr_7UhSN1zuXS'
REFUND_ID = 're_4qqhO89gsT'
ORDER_ID = 'ord_kEn1PlbGa'


def test_get_refund(client, response):
    """Retrieve a specific refund of a payment."""
    response.get('https://api.mollie.com/v2/payments/%s/refunds/%s' % (PAYMENT_ID, REFUND_ID), 'refund_single')
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payment_single')
    response.get('https://api.mollie.com/v2/orders/{order_id}'.format(order_id=ORDER_ID), 'order_single')

    refund = client.payment_refunds.with_parent_id(PAYMENT_ID).get(REFUND_ID)
    assert isinstance(refund, Refund)
    # properties
    assert refund.resource == 'refund'
    assert refund.id == REFUND_ID
    assert refund.amount == {'currency': 'EUR', 'value': '5.95'}
    assert refund.settlement_amount == {'currency': 'EUR', 'value': '10.00'}
    assert refund.description == 'Required quantity not in stock, refunding one photo book.'
    assert refund.status == Refund.STATUS_PENDING
    assert_list_object(refund.lines, OrderLine)
    assert refund.payment_id == PAYMENT_ID
    assert refund.order_id == ORDER_ID
    assert refund.created_at == '2018-03-14T17:09:02.0Z'
    # properties from _links
    assert refund.payment is not None
    assert refund.settlement is None
    assert isinstance(refund.order, Order)
    # additional methods
    assert refund.is_queued() is False
    assert refund.is_pending() is True
    assert refund.is_processing() is False
    assert refund.is_refunded() is False


def test_refund_get_related_payment(client, response):
    """Verify the related payment of a refund."""
    response.get('https://api.mollie.com/v2/payments/%s/refunds/%s' % (PAYMENT_ID, REFUND_ID), 'refund_single')
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payment_single')

    refund = client.payment_refunds.with_parent_id(PAYMENT_ID).get(REFUND_ID)
    payment = refund.payment
    assert isinstance(payment, Payment)
    assert payment.id == PAYMENT_ID


def test_create_refund(client, response):
    """Create a payment refund of a payment."""
    response.post('https://api.mollie.com/v2/payments/%s/refunds' % PAYMENT_ID, 'refund_single')

    data = {
        'amount': {'value': '5.95', 'currency': 'EUR'}
    }
    refund = client.payment_refunds.with_parent_id(PAYMENT_ID).create(data)
    assert isinstance(refund, Refund)
    assert refund.id == REFUND_ID


def test_get_single_refund_on_payment_object(client, response):
    """Retrieve a payment refund of a payment."""
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payment_single')
    response.get('https://api.mollie.com/v2/payments/%s/refunds/%s' % (PAYMENT_ID, REFUND_ID), 'refund_single')

    payment = client.payments.get(PAYMENT_ID)
    refund = client.payment_refunds.on(payment).get(REFUND_ID)
    assert isinstance(refund, Refund)
    assert refund.id == REFUND_ID


def test_list_refunds_on_payment_object(client, response):
    """Retrieve a list of payment refunds of a payment."""
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payment_single')
    response.get('https://api.mollie.com/v2/payments/%s/refunds' % PAYMENT_ID, 'refunds_list')

    payment = client.payments.get(PAYMENT_ID)
    refunds = client.payment_refunds.on(payment).list()
    assert_list_object(refunds, Refund)


def test_cancel_refund(client, response):
    """Cancel a refund of a payment."""
    response.delete('https://api.mollie.com/v2/payments/%s/refunds/%s' % (PAYMENT_ID, REFUND_ID), 'empty')

    canceled_refund = client.payment_refunds.with_parent_id(PAYMENT_ID).delete(REFUND_ID)
    assert canceled_refund == {}
