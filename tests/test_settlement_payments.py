from mollie.api.objects.payment import Payment

from .utils import assert_list_object

SETTLEMENT_ID = "stl_jDk30akdN"


def test_list_customer_payments(oauth_client, response):
    """Retrieve a list of payments related to a settlement id."""
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}/payments", "payments_list")

    settlement = oauth_client.settlements.get(SETTLEMENT_ID)
    payments = settlement.payments.list()
    assert_list_object(payments, Payment)
