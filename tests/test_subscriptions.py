from mollie.api.objects.subscription import Subscription

from .utils import assert_list_object


def test_list_subscriptions(client, response):
    """Retrieve a list of existing subscriptions."""
    response.get("https://api.mollie.com/v2/subscriptions", "subscriptions_list")

    subscriptions = client.subscriptions.list()
    assert_list_object(subscriptions, Subscription)
