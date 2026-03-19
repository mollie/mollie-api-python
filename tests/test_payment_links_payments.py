from mollie.api.objects.payment import Payment

from .utils import assert_list_object

PAYMENT_LINK_ID = "pl_4Y0eZitmBnQ6IDoMqZQKh"


def test_list_customer_payments(oauth_client, response):
    """Retrieve a list of payments related to a payment link id."""
    response.get(
        f"https://api.mollie.com/v2/payment-links/{PAYMENT_LINK_ID}",
        "payment_link_single",
    )
    response.get(
        f"https://api.mollie.com/v2/payment-links/{PAYMENT_LINK_ID}/payments",
        "payments_list",
    )

    payment_link = oauth_client.payment_links.get(PAYMENT_LINK_ID)
    payments = payment_link.payments.list()
    assert_list_object(payments, Payment)
