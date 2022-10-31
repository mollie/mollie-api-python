from mollie.api.objects.chargeback import Chargeback

from .utils import assert_list_object

PAYMENT_ID = "tr_7UhSN1zuXS"
SETTLEMENT_ID = "stl_jDk30akdN"
CHARGEBACK_ID = "chb_n9z0tp"


def test_list_settlement_chargebacks(oauth_client, response):
    """Get a list of chargebacks related to a settlement."""
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}/chargebacks", "chargebacks_list")

    settlement = oauth_client.settlements.get(SETTLEMENT_ID)
    chargebacks = settlement.chargebacks.list()
    assert_list_object(chargebacks, Chargeback)
