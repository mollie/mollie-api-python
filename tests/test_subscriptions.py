from mollie.api.objects.payment import Payment
from mollie.api.objects.subscription import Subscription

from .utils import assert_list_object

SUBSCRIPTION_ID = "sub_rVKGtNd6s3"
CUSTOMER_ID = "cst_8wmqcHMN4U"


def test_list_subscriptions(client, response):
    """Retrieve a list of existing subscriptions."""
    response.get("https://api.mollie.com/v2/subscriptions", "subscriptions_list")

    subscriptions = client.subscriptions.list()
    assert_list_object(subscriptions, Subscription)


def test_list_subscription_payments_by_parent_id(client, response):
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}/payments", "payments_list"
    )

    payments = client.subscription_payments.with_parent_id(CUSTOMER_ID, SUBSCRIPTION_ID).list()
    assert_list_object(payments, Payment)


def test_list_subscription_payments_by_parent_object(client, response):
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}", "subscription_single"
    )
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}/payments", "payments_list"
    )

    subscription = client.customer_subscriptions.with_parent_id(CUSTOMER_ID).get(SUBSCRIPTION_ID)
    payments = client.subscription_payments.on(subscription).list()
    assert_list_object(payments, Payment)
