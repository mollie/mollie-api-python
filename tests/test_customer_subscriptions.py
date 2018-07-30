from mollie.api.objects.list import List
from mollie.api.objects.subscription import Subscription
from mollie.api.objects.customer import Customer

CUSTOMER_ID = 'cst_8wmqcHMN4U'
SUBSCRIPTION_ID = 'sub_rVKGtNd6s3'


def test_customer_subscriptions_all(client, response):
    """Retrieve a list of subscriptions"""
    response.get('https://api.mollie.com/v2/customers/%s/subscriptions' % CUSTOMER_ID, 'subscription_all')

    subscriptions = client.customer_subscriptions.with_parent_id(CUSTOMER_ID).all()
    assert isinstance(subscriptions, List)
    assert subscriptions.count == 3
    iterated = 0
    iterated_subscription_ids = []
    for subscription in subscriptions:
        assert isinstance(subscription, Subscription)
        iterated += 1
        assert subscription.id is not None
        iterated_subscription_ids.append(subscription.id)
    assert iterated == subscriptions.count, 'Unexpected amount of subscriptions retrieved'
    assert len(set(iterated_subscription_ids)) == subscriptions.count, \
        'Unexpected amount of unique subscription ids retrieved'


def test_get_customer_subscription_by_id(client, response):
    """Retrieve a single subscription by ID """
    response.get('https://api.mollie.com/v2/customers/%s/subscriptions/%s' % (CUSTOMER_ID, SUBSCRIPTION_ID),
                 'subscription_single')

    subscription = client.customer_subscriptions.with_parent_id(CUSTOMER_ID).get(SUBSCRIPTION_ID)
    assert subscription.resource == 'subscription'
    assert subscription.id == SUBSCRIPTION_ID
    assert subscription.mode == 'live'
    assert subscription.created_at == '2016-06-01T12:23:34+00:00'
    assert subscription.is_active() is True
    assert subscription.is_suspended() is False
    assert subscription.is_pending() is False
    assert subscription.is_completed() is False
    assert subscription.is_canceled() is False
    assert subscription.amount['value'] == '25.00'
    assert subscription.amount['currency'] == 'EUR'
    assert subscription.times == 4
    assert subscription.interval == '3 months'
    assert subscription.description == 'Quarterly payment'
    assert subscription.method == 'ideal'
    assert subscription.webhook_url == 'https://webshop.example.org/payments/webhook'


def test_get_all_customer_subscriptions_by_customer_object(client, response):
    """Retrieve all subscriptions related to customer"""
    response.get('https://api.mollie.com/v2/customers/%s/subscriptions' % CUSTOMER_ID,
                 'subscription_all')
    response.get('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_single')

    customer = client.customers.get(CUSTOMER_ID)
    subscriptions = client.customer_subscriptions.on(customer).all()
    assert isinstance(subscriptions, List)

    iterated = 0
    for subscription in subscriptions:
        assert isinstance(subscription, Subscription)
        iterated += 1
    assert iterated == subscriptions.count, 'Unexpected amount of subscriptions retrieved'


def test_get_one_customer_subscription_by_customer_object(client, response):
    """Retrieve specific subscription related to customer"""
    response.get('https://api.mollie.com/v2/customers/%s/subscriptions/%s' % (CUSTOMER_ID, SUBSCRIPTION_ID),
                 'subscription_single')
    response.get('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_single')

    customer = client.customers.get(CUSTOMER_ID)
    subscription = client.customer_subscriptions.on(customer).get(SUBSCRIPTION_ID)
    assert subscription.customer.id == CUSTOMER_ID
    assert isinstance(subscription, Subscription)


def test_customer_subscription_get_related_customer(client, response):
    """Retrieve a related customer object from a subscription"""
    response.get('https://api.mollie.com/v2/customers/%s/subscriptions/%s' % (CUSTOMER_ID, SUBSCRIPTION_ID),
                 'subscription_single')
    response.get('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_single')

    subscription = client.customer_subscriptions.with_parent_id(CUSTOMER_ID).get(SUBSCRIPTION_ID)
    assert isinstance(subscription.customer, Customer)
    assert subscription.customer.id == CUSTOMER_ID


def test_cancel_customer_subscription(client, response):
    """Cancel a subscription by customer ID and subscription ID"""
    response.delete('https://api.mollie.com/v2/customers/%s/subscriptions/%s' % (CUSTOMER_ID, SUBSCRIPTION_ID),
                    'subscription_canceled', 200)

    subscription = client.customer_subscriptions.with_parent_id(CUSTOMER_ID).delete(SUBSCRIPTION_ID)
    assert subscription.status == 'canceled'
    assert subscription.canceled_at == '2018-08-01T11:04:21+00:00'


def test_create_customer_subscription(client, response):
    """create a subscription with customer object"""
    response.post('https://api.mollie.com/v2/customers/%s/subscriptions' % CUSTOMER_ID, 'subscription_single')
    data = {
        'amount': {'currency': 'EUR', 'value': '25.00'},
        'times': 4,
        'interval': '3 months',
        'description': 'Quarterly payment',
        'webhookUrl': 'https://webshop.example.org/subscriptions/webhook'
    }
    subscription = client.customer_subscriptions.with_parent_id(CUSTOMER_ID).create(data=data)
    assert subscription.id == SUBSCRIPTION_ID


def test_update_customer_subscription(client, response):
    """Update existing subscription of a customer"""
    response.patch('https://api.mollie.com/v2/customers/%s/subscriptions/%s' % (CUSTOMER_ID, SUBSCRIPTION_ID),
                   'subscription_updated')

    data = {
        'amount': {'currency': 'USD', 'value': '30.00'},
        'times': 42,
        'startDate': '2018-12-12',
        'description': 'Updated subscription',
        'webhookUrl': 'https://webshop.example.org/subscriptions/webhook'
    }
    subscription = client.customer_subscriptions.with_parent_id(CUSTOMER_ID).update(SUBSCRIPTION_ID, data)
    assert subscription.id == SUBSCRIPTION_ID
