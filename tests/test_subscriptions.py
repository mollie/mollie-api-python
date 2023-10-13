from responses import matchers

from mollie.api.objects.subscription import Subscription

from .utils import assert_list_object


def test_list_subscriptions(client, response):
    """Retrieve a list of existing subscriptions."""
    response.get("https://api.mollie.com/v2/subscriptions", "subscriptions_list")

    subscriptions = client.subscriptions.list()
    assert_list_object(subscriptions, Subscription)


def test_list_subscription_pagination(client, response):
    """Retrieve a list of paginated subscriptions."""
    response.get(
        "https://api.mollie.com/v2/subscriptions", "subscriptions_list", match=[matchers.query_string_matcher("")]
    )
    response.get(
        "https://api.mollie.com/v2/subscriptions",
        "subscriptions_list_more",
        match=[matchers.query_string_matcher("from=sub_rVKGtNd6s6")],
    )

    first_subscriptions_page = client.subscriptions.list()
    assert first_subscriptions_page.has_previous() is False
    assert first_subscriptions_page.has_next() is True

    second_subscriptions_page = first_subscriptions_page.get_next()
    assert_list_object(second_subscriptions_page, Subscription)

    subscription = next(second_subscriptions_page)
    assert subscription.id == "sub_rVKGtNd6s6"
