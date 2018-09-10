import pytest

from mollie.api.error import IdentifierError
from mollie.api.objects.customer import Customer
from mollie.api.objects.method import Method
from mollie.api.objects.subscription import Subscription

from .utils import assert_list_object

CUSTOMER_ID = 'cst_8wmqcHMN4U'
SUBSCRIPTION_ID = 'sub_rVKGtNd6s3'


def test_list_customer_subscriptions(client, response):
    """Retrieve a list of subscriptions."""
    response.get('https://api.mollie.com/v2/customers/%s/subscriptions' % CUSTOMER_ID, 'subscriptions_list')

    subscriptions = client.customer_subscriptions.with_parent_id(CUSTOMER_ID).list()
    assert_list_object(subscriptions, Subscription)


def test_get_customer_subscription_by_id(client, response):
    """Retrieve a single subscription by ID."""
    response.get('https://api.mollie.com/v2/customers/%s/subscriptions/%s' % (CUSTOMER_ID, SUBSCRIPTION_ID),
                 'subscription_single')
    response.get('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_single')

    subscription = client.customer_subscriptions.with_parent_id(CUSTOMER_ID).get(SUBSCRIPTION_ID)
    assert subscription.resource == 'subscription'
    assert subscription.id == SUBSCRIPTION_ID
    assert subscription.mode == 'live'
    assert subscription.created_at == '2016-06-01T12:23:34+00:00'
    assert subscription.amount == {'value': '25.00', 'currency': 'EUR'}
    assert subscription.times == 4
    assert subscription.interval == '3 months'
    assert subscription.description == 'Quarterly payment'
    assert subscription.method == Method.IDEAL
    assert subscription.webhook_url == 'https://webshop.example.org/payments/webhook'
    assert subscription.status == Subscription.STATUS_ACTIVE
    assert subscription.start_date is None
    assert subscription.canceled_at is None
    assert subscription.customer is not None
    assert subscription.is_active() is True
    assert subscription.is_suspended() is False
    assert subscription.is_pending() is False
    assert subscription.is_completed() is False
    assert subscription.is_canceled() is False


def test_list_customer_subscriptions_by_customer_object(client, response):
    """Retrieve a list of subscriptions related to customer."""
    response.get('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_single')
    response.get('https://api.mollie.com/v2/customers/%s/subscriptions' % CUSTOMER_ID,
                 'subscriptions_list')

    customer = client.customers.get(CUSTOMER_ID)
    subscriptions = client.customer_subscriptions.on(customer).list()
    assert_list_object(subscriptions, Subscription)


def test_get_customer_subscription_by_customer_object(client, response):
    """Retrieve specific subscription related to customer."""
    response.get('https://api.mollie.com/v2/customers/%s/subscriptions/%s' % (CUSTOMER_ID, SUBSCRIPTION_ID),
                 'subscription_single')
    response.get('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_single')

    customer = client.customers.get(CUSTOMER_ID)
    subscription = client.customer_subscriptions.on(customer).get(SUBSCRIPTION_ID)
    assert isinstance(subscription, Subscription)
    assert subscription.customer.id == CUSTOMER_ID


def test_customer_subscription_get_related_customer(client, response):
    """Retrieve a related customer object from a subscription."""
    response.get('https://api.mollie.com/v2/customers/%s/subscriptions/%s' % (CUSTOMER_ID, SUBSCRIPTION_ID),
                 'subscription_single')
    response.get('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_single')

    subscription = client.customer_subscriptions.with_parent_id(CUSTOMER_ID).get(SUBSCRIPTION_ID)
    assert isinstance(subscription.customer, Customer)
    assert subscription.customer.id == CUSTOMER_ID


def test_cancel_customer_subscription(client, response):
    """Cancel a subscription by customer ID and subscription ID."""
    response.delete('https://api.mollie.com/v2/customers/%s/subscriptions/%s' % (CUSTOMER_ID, SUBSCRIPTION_ID),
                    'subscription_canceled', 200)

    subscription = client.customer_subscriptions.with_parent_id(CUSTOMER_ID).delete(SUBSCRIPTION_ID)
    assert isinstance(subscription, Subscription)
    assert subscription.status == 'canceled'
    assert subscription.canceled_at == '2018-08-01T11:04:21+00:00'


def test_cancel_customer_subscription_invalid_id(client):
    """Verify that an invalid subscription id is validated and raises an error."""
    with pytest.raises(IdentifierError):
        client.customer_subscriptions.with_parent_id(CUSTOMER_ID).delete('invalid')


def test_create_customer_subscription(client, response):
    """Create a subscription with customer object."""
    response.post('https://api.mollie.com/v2/customers/%s/subscriptions' % CUSTOMER_ID, 'subscription_single')

    data = {
        'amount': {'currency': 'EUR', 'value': '25.00'},
        'times': 4,
        'interval': '3 months',
        'description': 'Quarterly payment',
        'webhookUrl': 'https://webshop.example.org/subscriptions/webhook'
    }
    subscription = client.customer_subscriptions.with_parent_id(CUSTOMER_ID).create(data=data)
    assert isinstance(subscription, Subscription)
    assert subscription.id == SUBSCRIPTION_ID


def test_update_customer_subscription(client, response):
    """Update existing subscription of a customer."""
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
    assert isinstance(subscription, Subscription)
    assert subscription.id == SUBSCRIPTION_ID
