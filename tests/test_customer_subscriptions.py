import pytest
from responses import matchers

from mollie.api.error import IdentifierError
from mollie.api.objects.customer import Customer
from mollie.api.objects.mandate import Mandate
from mollie.api.objects.method import Method
from mollie.api.objects.payment import Payment
from mollie.api.objects.profile import Profile
from mollie.api.objects.subscription import Subscription

from .utils import assert_list_object

CUSTOMER_ID = "cst_8wmqcHMN4U"
PROFILE_ID = "pfl_v9hTwCvYqw"
SUBSCRIPTION_ID = "sub_rVKGtNd6s3"
MANDATE_ID = "mdt_h3gAaD5zP"


def test_list_customer_subscriptions(client, response):
    """Retrieve a list of subscriptions."""
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions", "customer_subscriptions_list")

    customer = client.customers.get(CUSTOMER_ID)
    subscriptions = customer.subscriptions.list()
    assert_list_object(subscriptions, Subscription)


def test_list_customer_subscription_pagination(client, response):
    """Retrieve a list of paginated subscriptions."""
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions",
        "customer_subscriptions_list",
        match=[matchers.query_string_matcher("")],
    )
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions",
        "customer_subscriptions_list_more",
        match=[matchers.query_string_matcher("from=sub_rVKGtNd6s6")],
    )

    customer = client.customers.get(CUSTOMER_ID)
    first_subscriptions_page = customer.subscriptions.list()
    assert first_subscriptions_page.has_previous() is False
    assert first_subscriptions_page.has_next() is True

    second_subscriptions_page = first_subscriptions_page.get_next()
    assert_list_object(second_subscriptions_page, Subscription)

    subscription = next(second_subscriptions_page)
    assert subscription.id == "sub_rVKGtNd6s6"


def test_get_customer_subscription(client, response):
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}",
        "subscription_single",
    )

    customer = client.customers.get(CUSTOMER_ID)
    subscription = customer.subscriptions.get(SUBSCRIPTION_ID)
    assert isinstance(subscription, Subscription)
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
    assert subscription.mandate_id == "mdt_h3gAaD5zP"
    assert subscription.webhook_url == "https://webshop.example.org/payments/webhook"
    assert subscription.status == Subscription.STATUS_ACTIVE
    assert subscription.start_date == "2016-06-01"
    assert subscription.next_payment_date == "2016-09-01"
    assert subscription.canceled_at is None
    assert subscription.metadata == {"order_id": 1337}
    assert subscription.application_fee is None
    assert subscription.customer_id == CUSTOMER_ID
    assert subscription.is_active() is True
    assert subscription.is_suspended() is False
    assert subscription.is_pending() is False
    assert subscription.is_completed() is False
    assert subscription.is_canceled() is False


def test_get_customer_subscription_invalid_id(client, response):
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")

    customer = client.customers.get(CUSTOMER_ID)
    with pytest.raises(IdentifierError) as excinfo:
        customer.subscriptions.get("invalid")
    assert str(excinfo.value) == "Invalid subscription ID 'invalid', it should start with 'sub_'."


def test_customer_subscription_get_related_customer(client, response):
    """Retrieve a related customer object from a subscription."""
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}",
        "subscription_single",
    )

    customer = client.customers.get(CUSTOMER_ID)
    subscription = customer.subscriptions.get(SUBSCRIPTION_ID)
    related_customer = subscription.get_customer()
    assert isinstance(related_customer, Customer)
    assert related_customer.id == CUSTOMER_ID == customer.id


@pytest.mark.parametrize(
    "url_customer_id, actual_customer_id",
    [
        (CUSTOMER_ID, CUSTOMER_ID),
        ("cst_8.mqcHMN4U", "cst_8.mqcHMN4U"),
        ("cst_8.mqcHMN4U/", "cst_8.mqcHMN4U"),  # trailing slah in URL
    ],
)
def test_customer_subscription_get_related_customer_id_syntax(url_customer_id, actual_customer_id, client):
    data = {
        "resource": "subscription",
        "id": "sub_rVKGtNd6s3",
        "_links": {
            "customer": {
                "href": f"https://api.mollie.com/v2/customers/{url_customer_id}",
                "type": "application/hal+json",
            },
        },
    }
    subscription = Subscription(data, client)
    assert subscription.customer_id == actual_customer_id


def test_customer_subscription_get_related_profile(client, response):
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}",
        "subscription_single",
    )
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")

    customer = client.customers.get(CUSTOMER_ID)
    subscription = customer.subscriptions.get(SUBSCRIPTION_ID)
    profile = subscription.get_profile()
    assert isinstance(profile, Profile)
    assert profile.id == PROFILE_ID


def test_customer_subscription_get_related_mandate(client, response):
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}",
        "subscription_single",
    )
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/mandates/{MANDATE_ID}", "customer_mandate_single")

    customer = client.customers.get(CUSTOMER_ID)
    subscription = customer.subscriptions.get(SUBSCRIPTION_ID)
    mandate = subscription.get_mandate()
    assert isinstance(mandate, Mandate)
    assert mandate.id == MANDATE_ID


def test_cancel_customer_subscription(client, response):
    """Cancel a subscription by customer ID and subscription ID."""
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.delete(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}",
        "subscription_canceled",
        200,
    )

    customer = client.customers.get(CUSTOMER_ID)
    subscription = customer.subscriptions.delete(SUBSCRIPTION_ID)
    assert isinstance(subscription, Subscription)
    assert subscription.status == "canceled"
    assert subscription.canceled_at == "2018-08-01T11:04:21+00:00"


def test_cancel_customer_subscription_invalid_id(client, response):
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")

    customer = client.customers.get(CUSTOMER_ID)
    with pytest.raises(IdentifierError) as excinfo:
        customer.subscriptions.delete("invalid")
    assert str(excinfo.value) == "Invalid subscription ID 'invalid', it should start with 'sub_'."


def test_create_customer_subscription(client, response):
    """Create a subscription with customer object."""
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.post(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions", "subscription_single")

    data = {
        "amount": {"currency": "EUR", "value": "25.00"},
        "times": 4,
        "interval": "3 months",
        "description": "Quarterly payment",
        "webhookUrl": "https://webshop.example.org/subscriptions/webhook",
    }
    customer = client.customers.get(CUSTOMER_ID)
    subscription = customer.subscriptions.create(data=data)
    assert isinstance(subscription, Subscription)
    assert subscription.id == SUBSCRIPTION_ID


def test_update_customer_subscription(client, response):
    """Update existing subscription of a customer."""
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.patch(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}",
        "subscription_updated",
    )

    customer = client.customers.get(CUSTOMER_ID)
    data = {
        "amount": {"currency": "USD", "value": "30.00"},
        "times": 42,
        "startDate": "2018-12-12",
        "description": "Updated subscription",
        "webhookUrl": "https://webshop.example.org/subscriptions/webhook",
    }
    subscription = customer.subscriptions.update(SUBSCRIPTION_ID, data)
    assert isinstance(subscription, Subscription)
    assert subscription.id == SUBSCRIPTION_ID


def test_update_customer_subscription_invalid_id(client, response):
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")

    customer = client.customers.get(CUSTOMER_ID)
    data = {}
    with pytest.raises(IdentifierError) as excinfo:
        customer.subscriptions.update("invalid", data)
    assert str(excinfo.value) == "Invalid subscription ID 'invalid', it should start with 'sub_'."


def test_customer_subscription_get_related_payments(client, response):
    """Retrieve a list of payments related to the subscription."""
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}",
        "subscription_single",
    )
    response.get(
        f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/subscriptions/{SUBSCRIPTION_ID}/payments",
        "payments_list",
    )
    customer = client.customers.get(CUSTOMER_ID)
    subscription = customer.subscriptions.get(SUBSCRIPTION_ID)
    payments = subscription.payments.list()
    assert_list_object(payments, Payment)
