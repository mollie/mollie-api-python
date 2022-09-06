import re

import pytest

from mollie.api.error import RemovedIn215Warning
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


def test_list_subscription_payments(client, response):
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}", "subscription_single"
    )
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}/payments", "payments_list"
    )

    subscription = client.subscriptions.with_parent_id(CUSTOMER_ID).get(SUBSCRIPTION_ID)
    payments = subscription.payments
    assert_list_object(payments, Payment)


def test_list_subscription_payments_through_deprecated_path_raises_warning(client, response):
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}/payments", "payments_list"
    )
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}", "subscription_single"
    )

    with pytest.warns(
        RemovedIn215Warning,
        match=re.escape(
            "Using client.subscription_payments is deprecated, use <subscription object>.payments to retrieve "
            "Subscription payments."
        ),
    ):
        client.subscription_payments.with_parent_id(CUSTOMER_ID, SUBSCRIPTION_ID).list()

    subscription = client.subscriptions.with_parent_id(CUSTOMER_ID).get(SUBSCRIPTION_ID)
    with pytest.warns(
        RemovedIn215Warning,
        match=re.escape(
            "Using client.subscription_payments is deprecated, use <subscription object>.payments to retrieve "
            "Subscription payments."
        ),
    ):
        client.subscription_payments.on(subscription).list()
