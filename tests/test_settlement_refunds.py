from mollie.api.objects.refund import Refund

from .utils import assert_list_object

SETTLEMENT_ID = "stl_jDk30akdN"


def test_list_refunds_on_settlement_object(oauth_client, response):
    """Retrieve a list of payment refunds of a payment."""
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}/refunds", "refunds_list")

    settlement = oauth_client.settlements.get(SETTLEMENT_ID)
    refunds = settlement.refunds.list()
    assert_list_object(refunds, Refund)
