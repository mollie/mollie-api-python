from mollie.api.objects.list import List
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
    assert customer.name == 'Customer A'
    assert customer.email == 'customer@example.org'
    assert customer.id is not None
    assert customer.resource == 'customer'
    assert customer.created_at is not None
    assert customer.metadata is None
    assert customer.locale == 'nl_NL'
    assert customer.mode == 'test'


def test_update_customer(client, response):
    response.patch('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_updated')

    updated_customer = client.customers.update(CUSTOMER_ID, {
        'name': 'Updated Customer A',
        'email': 'updated-customer@example.org',
    })
    assert updated_customer.name == 'Updated Customer A'
    assert updated_customer.email == 'updated-customer@example.org'


def test_delete_customers(client, response):
    response.delete('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'empty')

    deleted_customer = client.customers.delete('cst_8wmqcHMN4U')
    assert deleted_customer == {}


def test_customers_all(client, response):
    response.get('https://api.mollie.com/v2/customers', 'customer_multiple')

    customers = client.customers.all()
    assert customers.count == 3
    iterated = 0
    for customer in customers:
        iterated += 1
        assert customer.id is not None
        assert customer.mode is not None
        assert customer.resource is not None
        assert customer.name is not None
        assert customer.email is not None
        assert customer.locale is not None
        assert customer.created_at is not None
    assert iterated == 3


def test_customer_get_mandates(client, response):
    """Retrieve related mandates for a customer."""
    response.get('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_updated')
    response.get('https://api.mollie.com/v2/customers/%s/mandates' % CUSTOMER_ID, 'customer_mandates_multiple')

    customer = client.customers.get(CUSTOMER_ID)
    mandates = customer.mandates
    assert mandates.__class__.__name__ == 'List'
    iterated = 0
    for mandate in mandates:
        assert mandate.__class__.__name__ == 'Mandate'
        iterated += 1
    assert iterated == mandates.count


def test_get_all_subscription_from_customer_object(client, response):
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
