import pytest

from mollie.api.objects.chargeback import Chargeback
from mollie.api.objects.customer import Customer
from mollie.api.objects.list import List
from mollie.api.objects.mandate import Mandate
from mollie.api.objects.method import Method
from mollie.api.objects.payment import Payment
from mollie.api.objects.refund import Refund
from mollie.api.objects.subscription import Subscription

PAYMENT_ID = 'tr_7UhSN1zuXS'
REFUND_ID = 're_4qqhO89gsT'
CHARGEBACK_ID = 'chb_n9z0tp'
CUSTOMER_ID = 'cst_8wmqcHMN4U'
SETTLEMENT_ID = 'stl_jDk30akdN'
MANDATE_ID = 'mdt_h3gAaD5zP'
SUBSCRIPTION_ID = 'sub_rVKGtNd6s3'


def test_get_all_payments(client, response):
    """Retrieve all existing payments."""
    response.get('https://api.mollie.com/v2/payments', 'payments_list')

    payments = client.payments.all()
    assert isinstance(payments, List)
    assert payments.count == 3

    iterated = 0
    iterated_payment_ids = []
    for payment in payments:
        assert isinstance(payment, Payment)
        assert payment.id is not None
        iterated += 1
        iterated_payment_ids.append(payment.id)
    assert iterated == payments.count, 'Unexpected amount of payments retrieved'
    assert len(set(iterated_payment_ids)) == payments.count, 'Unexpected unique payment ids retrieved'


def test_create_payment(client, response):
    """Create a new payment."""
    response.post('https://api.mollie.com/v2/payments', 'payment_single')

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
    """Cancel existing payment."""
    response.delete('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payment_canceled', 200)

    canceled_payment = client.payments.delete(PAYMENT_ID)
    assert isinstance(canceled_payment, Payment)
    assert canceled_payment.is_canceled() is True
    assert canceled_payment.canceled_at == '2018-03-20T09:28:37+00:00'
    assert canceled_payment.id == PAYMENT_ID


def test_get_single_payment(client, response):
    """Retrieve a single payment by payment id."""
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payment_single')
    response.get('https://api.mollie.com/v2/payments/%s/refunds' % PAYMENT_ID, 'refunds_list')
    response.get('https://api.mollie.com/v2/payments/%s/chargebacks' % PAYMENT_ID, 'chargebacks_list')
    response.get('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_single')
    response.get('https://api.mollie.com/v2/customers/{cust}/mandates/{man}'.format(
        cust=CUSTOMER_ID, man=MANDATE_ID), 'customer_mandate_single')
    response.get('https://api.mollie.com/v2/customers/{cust}/subscriptions/{sub}'.format(
        cust=CUSTOMER_ID, sub=SUBSCRIPTION_ID), 'subscription_single')

    payment = client.payments.get(PAYMENT_ID)
    assert isinstance(payment, Payment)
    # properties
    assert payment.resource == 'payment'
    assert payment.id == PAYMENT_ID
    assert payment.mode == 'test'
    assert payment.created_at == '2018-03-20T09:13:37+00:00'
    assert payment.status == Payment.STATUS_OPEN
    assert payment.is_cancelable is False
    assert payment.paid_at is None
    assert payment.canceled_at is None
    assert payment.expires_at == '2018-03-20T09:28:37+00:00'
    assert payment.expired_at is None
    assert payment.failed_at is None
    assert payment.amount == {'value': '10.00', 'currency': 'EUR'}
    assert payment.amount_refunded is None
    assert payment.amount_remaining is None
    assert payment.description == 'Order #12345'
    assert payment.redirect_url == 'https://webshop.example.org/order/12345/'
    assert payment.webhook_url == 'https://webshop.example.org/payments/webhook/'
    assert payment.method == Method.IDEAL
    assert payment.metadata == {'order_id': '12345'}
    assert payment.locale is None
    assert payment.country_code is None
    assert payment.profile_id == 'pfl_QkEhN94Ba'
    assert payment.settlement_amount is None
    assert payment.settlement_id is None
    assert payment.customer_id == CUSTOMER_ID
    assert payment.sequence_type == Payment.SEQUENCETYPE_RECURRING
    assert payment.mandate_id == MANDATE_ID
    assert payment.subscription_id == SUBSCRIPTION_ID
    assert payment.order_id is None
    assert payment.application_fee is None
    assert payment.details is None
    # properties from _links
    assert payment.checkout_url == 'https://www.mollie.com/payscreen/select-method/7UhSN1zuXS'
    assert payment.refunds is not None
    assert payment.chargebacks is not None
    assert payment.settlement is None
    assert payment.mandate is not None
    assert payment.subscription is not None
    assert payment.customer is not None
    assert payment.order is None
    # additional methods
    assert payment.is_open() is True
    assert payment.is_pending() is False
    assert payment.is_canceled() is False
    assert payment.is_expired() is False
    assert payment.is_paid() is False
    assert payment.is_failed() is False
    assert payment.has_refunds() is True
    assert payment.can_be_refunded() is False
    assert payment.has_sequence_type_first() is False
    assert payment.has_sequence_type_recurring() is True


def test_payment_get_related_refunds(client, response):
    """Retrieve a list of all refunds related to a payment."""
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payment_single')
    response.get('https://api.mollie.com/v2/payments/%s/refunds' % PAYMENT_ID, 'refunds_list')

    payment = client.payments.get(PAYMENT_ID)
    refunds = payment.refunds
    assert isinstance(refunds, List)
    assert refunds.count == 1

    iterated = 0
    iterated_refund_ids = []
    for refund in refunds:
        assert isinstance(refund, Refund)
        iterated += 1
        assert refund.id is not None
        iterated_refund_ids.append(refund.id)
    assert iterated == refunds.count, 'Unexpected amount of refunds retrieved'
    assert len(set(iterated_refund_ids)) == refunds.count, 'Expected unique refund ids retrieved'


def test_payment_get_related_chargebacks(client, response):
    """Get chargebacks related to payment id."""
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payment_single')
    response.get('https://api.mollie.com/v2/payments/%s/chargebacks' % PAYMENT_ID, 'chargebacks_list')

    payment = client.payments.get(PAYMENT_ID)
    chargebacks = payment.chargebacks

    assert isinstance(chargebacks, List)
    iterated = 0
    for chargeback in chargebacks:
        assert isinstance(chargeback, Chargeback)
        iterated += 1
    assert iterated == chargebacks.count


@pytest.mark.xfail(strict=True, reason="Settlement API is not yet implemented")
def test_payment_get_related_settlement(client, response):
    """Get the settlement related to the payment."""
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payment_single')
    response.get('https://api.mollie.com/v2/settlements/%s' % SETTLEMENT_ID, 'settlement_single')

    payment = client.payments.get(PAYMENT_ID)
    settlement = payment.settlement
    # assert isinstance(settlement, Settlement)
    assert settlement.id == SETTLEMENT_ID


def test_payment_get_related_mandate(client, response):
    """Get the mandate related to the payment."""
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payment_single')
    response.get('https://api.mollie.com/v2/customers/{cust}/mandates/{man}'.format(
        cust=CUSTOMER_ID, man=MANDATE_ID), 'customer_mandate_single')

    payment = client.payments.get(PAYMENT_ID)
    mandate = payment.mandate
    assert isinstance(mandate, Mandate)
    assert mandate.id == MANDATE_ID


def test_payment_get_related_subscription(client, response):
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payment_single')
    response.get('https://api.mollie.com/v2/customers/{cust}/subscriptions/{sub}'.format(
        cust=CUSTOMER_ID, sub=SUBSCRIPTION_ID), 'subscription_single')

    payment = client.payments.get(PAYMENT_ID)
    subscription = payment.subscription
    assert isinstance(subscription, Subscription)
    assert subscription.id == SUBSCRIPTION_ID


def test_payment_get_related_customer(client, response):
    """Get customer related to payment."""
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payment_single')
    response.get('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_single')

    payment = client.payments.get(PAYMENT_ID)
    customer = payment.customer
    assert isinstance(customer, Customer)
    assert customer.id == CUSTOMER_ID
