import pytest

from mollie.api.objects.subscription import Subscription

from .utils import assert_list_object


def test_list_customers(client, response):
    """Retrieve a list of existing subscriptions."""
    response.get('https://api.mollie.com/v2/subscriptions', 'subscriptions_list')

    subscriptions = client.subscriptions.list()
    assert_list_object(subscriptions, Subscription)


def test_create_subscription(client):
    with pytest.raises(NotImplementedError, match='The endpoint "create" is not supported.'):
        client.subscriptions.create()


def test_get_subscription(client):
    with pytest.raises(NotImplementedError, match='The endpoint "get" is not supported.'):
        client.subscriptions.get('sub_rVKGtNd6s3')


def test_update_subscription(client):
    with pytest.raises(NotImplementedError, match='The endpoint "update" is not supported.'):
        client.subscriptions.update('sub_rVKGtNd6s3')


def test_delete_subscription(client):
    with pytest.raises(NotImplementedError, match='The endpoint "delete" is not supported.'):
        client.subscriptions.delete('sub_rVKGtNd6s3')
