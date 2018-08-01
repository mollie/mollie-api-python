from mollie.api.objects.customer import Customer
from mollie.api.objects.list import List
from mollie.api.objects.mandate import Mandate
from mollie.api.objects.payment import Payment
from mollie.api.objects.subscription import Subscription

CUSTOMER_ID = 'cst_8wmqcHMN4U'


def test_create_customer(client, response):
    """Create a new customer."""
    response.post('https://api.mollie.com/v2/customers', 'customer_new')

    customer = client.customers.create({
        'name': 'Customer A',
        'email': 'customer@example.org',
        'locale': 'nl_NL',
    })
    assert isinstance(customer, Customer)
    assert customer.id == CUSTOMER_ID


def test_update_customer(client, response):
    """Update an existing customer"""
    response.patch('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_updated')

    updated_customer = client.customers.update(CUSTOMER_ID, {
        'name': 'Updated Customer A',
        'email': 'updated-customer@example.org',
    })
    assert updated_customer.name == 'Updated Customer A'
    assert updated_customer.email == 'updated-customer@example.org'


def test_delete_customers(client, response):
    """Delete a customer"""
    response.delete('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'empty')

    deleted_customer = client.customers.delete('cst_8wmqcHMN4U')
    assert deleted_customer == {}


def test_customers_all(client, response):
    """Retrieve a list of all existing customers"""
    response.get('https://api.mollie.com/v2/customers', 'customers_multiple')

    customers = client.customers.all()
    assert isinstance(customers, List)
    assert customers.count == 3
    iterated = 0
    iterated_customer_ids = []
    for customer in customers:
        assert isinstance(customer, Customer)
        iterated += 1
        assert customer.id is not None
        iterated_customer_ids.append(customer.id)
    assert iterated == customers.count, 'Unexpected amount of customers retrieved'
    assert len(set(iterated_customer_ids)) == customers.count, 'Unexpected amount of unique customer ids retrieved'


def test_customer_get(client, response):
    """Retrieve a single customer."""
    response.get('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_new')
    customer = client.customers.get(CUSTOMER_ID)
    assert isinstance(customer, Customer)
    assert customer.id == CUSTOMER_ID
    assert customer.name == 'Customer A'
    assert customer.email == 'customer@example.org'
    assert customer.created_at == '2018-04-06T13:10:19.0Z'
    assert customer.metadata == {'orderId': '12345'}
    assert customer.locale == 'nl_NL'
    assert customer.mode == 'test'


def test_customer_get_related_mandates(client, response):
    """Retrieve related mandates for a customer."""
    response.get('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_updated')
    response.get('https://api.mollie.com/v2/customers/%s/mandates' % CUSTOMER_ID, 'customer_mandates_multiple')

    customer = client.customers.get(CUSTOMER_ID)
    mandates = customer.mandates
    assert isinstance(mandates, List)
    iterated = 0
    for mandate in mandates:
        assert isinstance(mandate, Mandate)
        iterated += 1
    assert iterated == mandates.count


def test_customer_get_related_subscriptions(client, response):
    """Retrieve related subscriptions for a customer"""
    response.get('https://api.mollie.com/v2/customers/%s/subscriptions' % CUSTOMER_ID,
                 'subscription_all')
    response.get('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_single')

    customer = client.customers.get(CUSTOMER_ID)
    subscriptions = customer.subscriptions
    assert isinstance(subscriptions, List)

    iterated = 0
    for subscription in subscriptions:
        assert isinstance(subscription, Subscription)
        iterated += 1
    assert iterated == subscriptions.count, 'Unexpected amount of subscriptions retrieved'


def test_customer_get_related_payments(client, response):
    """Retrieve related payments for a customer"""
    response.get('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_new')
    response.get('https://api.mollie.com/v2/customers/%s/payments' % CUSTOMER_ID, 'customer_payments_multiple')

    customer = client.customers.get(CUSTOMER_ID)
    payments = customer.payments
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
