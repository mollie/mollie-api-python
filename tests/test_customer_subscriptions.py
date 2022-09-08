import re

import pytest

from mollie.api.error import IdentifierError, RemovedIn215Warning
from mollie.api.objects.customer import Customer
from mollie.api.objects.method import Method
from mollie.api.objects.payment import Payment
from mollie.api.objects.profile import Profile
from mollie.api.objects.subscription import Subscription

from .utils import assert_list_object

CUSTOMER_ID = "cst_8wmqcHMN4U"
PROFILE_ID = "pfl_v9hTwCvYqw"
SUBSCRIPTION_ID = "sub_rVKGtNd6s3"


def test_list_customer_subscriptions(client, response):
    """Retrieve a list of subscriptions."""
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions", "subscriptions_customer_list")

    subscriptions = client.subscriptions.with_parent_id(CUSTOMER_ID).list()
    assert_list_object(subscriptions, Subscription)


def test_list_customer_subscriptions_by_deprecated_path_raises_warning(client, response):
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions", "subscriptions_customer_list")
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")

    with pytest.warns(
        RemovedIn215Warning,
        match=re.escape(
            "Using client.customer_subscriptions is deprecated, use "
            "client.payments.with_parent_id(<customer_id>).list() to retrieve Customer payments."
        ),
    ):
        client.customer_subscriptions.with_parent_id(CUSTOMER_ID).list()

    customer = client.customers.get(CUSTOMER_ID)
    with pytest.warns(
        RemovedIn215Warning,
        match=re.escape(
            "Using client.customer_subscriptions is deprecated, use client.payments.on(<customer_object>).list() to "
            "retrieve Customer payments."
        ),
    ):
        client.customer_subscriptions.on(customer).list()


def test_get_customer_subscription_by_id(client, response):
    """Retrieve a single subscription by ID."""
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}",
        "subscription_single",
    )
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")

    subscription = client.subscriptions.with_parent_id(CUSTOMER_ID).get(SUBSCRIPTION_ID)
    assert subscription.resource == "subscription"
    assert subscription.id == SUBSCRIPTION_ID
    assert subscription.mode == "live"
    assert subscription.created_at == "2016-06-01T12:23:34+00:00"
    assert subscription.amount == {"value": "25.00", "currency": "EUR"}
    assert subscription.times == 4
    assert subscription.times_remaining == 4
    assert subscription.interval == "3 months"
    assert subscription.description == "Quarterly payment"
    assert subscription.method == Method.IDEAL
    assert subscription.mandate_id == "mdt_38HS4fsS"
    assert subscription.webhook_url == "https://webshop.example.org/payments/webhook"
    assert subscription.status == Subscription.STATUS_ACTIVE
    assert subscription.start_date == "2016-06-01"
    assert subscription.next_payment_date == "2016-09-01"
    assert subscription.canceled_at is None
    assert subscription.customer is not None
    assert subscription.metadata == {"order_id": 1337}
    assert subscription.application_fee is None
    assert subscription.is_active() is True
    assert subscription.is_suspended() is False
    assert subscription.is_pending() is False
    assert subscription.is_completed() is False
    assert subscription.is_canceled() is False


def test_list_customer_subscriptions_by_customer_object(client, response):
    """Retrieve a list of subscriptions related to customer."""
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions", "subscriptions_customer_list")

    customer = client.customers.get(CUSTOMER_ID)
    subscriptions = client.subscriptions.on(customer).list()
    assert_list_object(subscriptions, Subscription)


def test_get_customer_subscription_by_customer_object(client, response):
    """Retrieve specific subscription related to customer."""
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}",
        "subscription_single",
    )
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")

    customer = client.customers.get(CUSTOMER_ID)
    subscription = client.subscriptions.on(customer).get(SUBSCRIPTION_ID)
    assert isinstance(subscription, Subscription)
    assert subscription.customer.id == CUSTOMER_ID


def test_customer_subscription_get_related_customer(client, response):
    """Retrieve a related customer object from a subscription."""
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}",
        "subscription_single",
    )
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")

    subscription = client.subscriptions.with_parent_id(CUSTOMER_ID).get(SUBSCRIPTION_ID)
    assert isinstance(subscription.customer, Customer)
    assert subscription.customer.id == CUSTOMER_ID


def test_customer_subscription_get_related_profile(client, response):
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}",
        "subscription_single",
    )
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")

    subscription = client.subscriptions.with_parent_id(CUSTOMER_ID).get(SUBSCRIPTION_ID)
    profile = subscription.profile
    assert isinstance(profile, Profile)
    assert profile.id == PROFILE_ID


def test_cancel_customer_subscription(client, response):
    """Cancel a subscription by customer ID and subscription ID."""
    response.delete(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}",
        "subscription_canceled",
        200,
    )

    subscription = client.subscriptions.with_parent_id(CUSTOMER_ID).delete(SUBSCRIPTION_ID)
    assert isinstance(subscription, Subscription)
    assert subscription.status == "canceled"
    assert subscription.canceled_at == "2018-08-01T11:04:21+00:00"


def test_cancel_customer_subscription_invalid_id(client):
    """Verify that an invalid subscription id is validated and raises an error."""
    with pytest.raises(IdentifierError):
        client.subscriptions.with_parent_id(CUSTOMER_ID).delete("invalid")


def test_create_customer_subscription(client, response):
    """Create a subscription with customer object."""
    response.post(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions", "subscription_single")

    data = {
        "amount": {"currency": "EUR", "value": "25.00"},
        "times": 4,
        "interval": "3 months",
        "description": "Quarterly payment",
        "webhookUrl": "https://webshop.example.org/subscriptions/webhook",
    }
    subscription = client.subscriptions.with_parent_id(CUSTOMER_ID).create(data=data)
    assert isinstance(subscription, Subscription)
    assert subscription.id == SUBSCRIPTION_ID


def test_update_customer_subscription(client, response):
    """Update existing subscription of a customer."""
    response.patch(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}",
        "subscription_updated",
    )

    data = {
        "amount": {"currency": "USD", "value": "30.00"},
        "times": 42,
        "startDate": "2018-12-12",
        "description": "Updated subscription",
        "webhookUrl": "https://webshop.example.org/subscriptions/webhook",
    }
    subscription = client.subscriptions.with_parent_id(CUSTOMER_ID).update(SUBSCRIPTION_ID, data)
    assert isinstance(subscription, Subscription)
    assert subscription.id == SUBSCRIPTION_ID


def test_customer_subscription_get_related_payments(client, response):
    """Retrieve a list of payments related to the subscription."""
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}",
        "subscription_single",
    )
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}/payments",
        "payments_list",
    )
    subscription = client.subscriptions.with_parent_id(CUSTOMER_ID).get(SUBSCRIPTION_ID)
    payments = subscription.payments
    assert_list_object(payments, Payment)


def test_get_customer_subscriptions_with_invalid_parent_raises_error(client):
    with pytest.raises(
        IdentifierError,
        match=re.escape("Invalid Parent, the parent of a Capture should be a Payment or a Settlement."),
    ):
        client.subscriptions.with_parent_id("invalid").get(SUBSCRIPTION_ID)
