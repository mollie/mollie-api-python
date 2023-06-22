from mollie.api.objects.chargeback import Chargeback

from .utils import assert_list_object

PAYMENT_ID = "tr_7UhSN1zuXS"
SETTLEMENT_ID = "stl_jDk30akdN"
CHARGEBACK_ID = "chb_n9z0tp"


def test_list_settlement_chargebacks(oauth_client, response):
    """Get a list of chargebacks related to a settlement."""
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}/chargebacks", "settlement_chargebacks_list")
    response.get(
        f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}/chargebacks?limit=1&from=chb_n9z0tq",
        "settlement_chargebacks_list_more",
    )

    settlement = oauth_client.settlements.get(SETTLEMENT_ID)
    chargebacks = settlement.chargebacks.list()
    assert_list_object(chargebacks, Chargeback)

    assert chargebacks.has_next()
    more_chargebacks = chargebacks.get_next()
    assert_list_object(more_chargebacks, Chargeback)
