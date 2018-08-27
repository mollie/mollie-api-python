from mollie.api.objects.payment import Payment

from .utils import assert_list_object

CUSTOMER_ID = 'cst_8wmqcHMN4U'


def test_list_customer_payments(client, response):
    """Retrieve a list of payments related to a customer id."""
    response.get('https://api.mollie.com/v2/customers/%s/payments' % CUSTOMER_ID, 'customer_payments_multiple')

    payments = client.customer_payments.with_parent_id(CUSTOMER_ID).list()
    assert_list_object(payments, Payment)


def test_list_customer_payments_by_object(client, response):
    response.get('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_single')
    response.get('https://api.mollie.com/v2/customers/%s/payments' % CUSTOMER_ID, 'customer_payments_multiple')

    customer = client.customers.get(CUSTOMER_ID)
    payments = client.customer_payments.on(customer).list()
    assert_list_object(payments, Payment)


def test_create_customer_payment(client, response):
    """Create a customer payment."""
    response.post('https://api.mollie.com/v2/customers/%s/payments' % CUSTOMER_ID, 'payment_single')

    payment = client.customer_payments.with_parent_id(CUSTOMER_ID).create(
        {
            'amount': {'currency': 'EUR', 'value': '10.00'},
            'description': 'Order #12345',
            'redirectUrl': 'https://webshop.example.org/order/12345/',
            'webhookUrl': 'https://webshop.example.org/payments/webhook/',
            'method': 'ideal',
        })
    assert isinstance(payment, Payment)
    assert payment.customer_id == CUSTOMER_ID
