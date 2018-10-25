import pytest

from mollie.api.error import IdentifierError
from mollie.api.objects.chargeback import Chargeback
from mollie.api.objects.customer import Customer
from mollie.api.objects.mandate import Mandate
from mollie.api.objects.method import Method
from mollie.api.objects.order import Order
from mollie.api.objects.payment import Payment
from mollie.api.objects.refund import Refund
from mollie.api.objects.subscription import Subscription

from .utils import assert_list_object

PAYMENT_ID = 'tr_7UhSN1zuXS'
REFUND_ID = 're_4qqhO89gsT'
CHARGEBACK_ID = 'chb_n9z0tp'
CUSTOMER_ID = 'cst_8wmqcHMN4U'
SETTLEMENT_ID = 'stl_jDk30akdN'
MANDATE_ID = 'mdt_h3gAaD5zP'
SUBSCRIPTION_ID = 'sub_rVKGtNd6s3'
ORDER_ID = 'ord_kEn1PlbGa'


def test_list_payments(client, response):
    """Retrieve a list of payments."""
    response.get('https://api.mollie.com/v2/payments', 'payments_list')

    payments = client.payments.list()
    assert_list_object(payments, Payment)


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


def test_cancel_payment_invalid_id(client):
    """Verify that an invalid payment id is validated and an error is raised."""
    with pytest.raises(IdentifierError):
        client.payments.delete('invalid')


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
    response.get('https://api.mollie.com/v2/orders/{order_id}'.format(order_id=ORDER_ID), 'order_single')

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
    assert payment.authorized_at is None
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
    assert isinstance(payment.order, Order)
    # additional methods
    assert payment.is_open() is True
    assert payment.is_pending() is False
    assert payment.is_canceled() is False
    assert payment.is_expired() is False
    assert payment.is_paid() is False
    assert payment.is_failed() is False
    assert payment.is_authorized() is False
    assert payment.has_refunds() is True
    assert payment.can_be_refunded() is False
    assert payment.has_sequence_type_first() is False
    assert payment.has_sequence_type_recurring() is True


def test_payment_get_related_refunds(client, response):
    """Retrieve a list of refunds related to a payment."""
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payment_single')
    response.get('https://api.mollie.com/v2/payments/%s/refunds' % PAYMENT_ID, 'refunds_list')

    payment = client.payments.get(PAYMENT_ID)
    refunds = payment.refunds
    assert_list_object(refunds, Refund)


def test_payment_get_related_chargebacks(client, response):
    """Get chargebacks related to payment id."""
    response.get('https://api.mollie.com/v2/payments/%s' % PAYMENT_ID, 'payment_single')
    response.get('https://api.mollie.com/v2/payments/%s/chargebacks' % PAYMENT_ID, 'chargebacks_list')

    payment = client.payments.get(PAYMENT_ID)
    chargebacks = payment.chargebacks
    assert_list_object(chargebacks, Chargeback)


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
