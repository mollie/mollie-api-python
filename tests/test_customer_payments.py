from mollie.api.objects.list import List
from mollie.api.objects.payment import Payment

CUSTOMER_ID = 'cst_8wmqcHMN4U'


def test_get_all_customer_payments(client, response):
    """Retrieve a list of payments related to a customer id"""
    response.get('https://api.mollie.com/v2/customers/%s/payments' % CUSTOMER_ID, 'customer_payments_multiple')

    payments = client.customer_payments.with_parent_id(CUSTOMER_ID).all()
    assert isinstance(payments, List)
    assert payments.count == 1
    iterated = 0
    iterated_payment_ids = []
    for payment in payments:
        iterated += 1
        assert isinstance(payment, Payment)
        assert payment.id is not None
        iterated_payment_ids.append(payment.id)
    assert iterated == payments.count, 'Unexpected amount of payments retrieved'
    assert len(set(iterated_payment_ids)) == payments.count, 'Unexpected unique payment ids retrieved'


def test_create_customer_payments(client, response):
    """Create a customer payment"""
    response.post('https://api.mollie.com/v2/customers/%s/payments' % CUSTOMER_ID, 'payments_create')

    payment = client.customer_payments.with_parent_id(CUSTOMER_ID).create(
        {
            'amount': {'currency': 'EUR', 'value': '10.00'},
            'description': 'Order #12345',
            'redirectUrl': 'https://webshop.example.org/order/12345/',
            'webhookUrl': 'https://webshop.example.org/payments/webhook/',
            'method': 'ideal',
        })
    assert payment.customer_id == CUSTOMER_ID
