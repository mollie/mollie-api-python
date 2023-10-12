from responses import matchers

from mollie.api.objects.chargeback import Chargeback

from .utils import assert_list_object

PAYMENT_ID = "tr_7UhSN1zuXS"
SETTLEMENT_ID = "stl_jDk30akdN"


def test_list_settlement_chargebacks(oauth_client, response):
    """Get a list of chargebacks related to a settlement."""
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}/chargebacks", "settlement_chargebacks_list")

    settlement = oauth_client.settlements.get(SETTLEMENT_ID)
    chargebacks = settlement.chargebacks.list()
    assert_list_object(chargebacks, Chargeback)


def test_list_settlement_chargebacks_pagination(oauth_client, response):
    """Retrieve a list of paginated settlement chargebacks."""
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")

    response.get(
        f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}/chargebacks",
        "settlement_chargebacks_list",
        match=[matchers.query_string_matcher("")],
    )
    response.get(
        f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}/chargebacks",
        "settlement_chargebacks_list_more",
        match=[matchers.query_string_matcher("from=chb_n9z0tq")],
    )

    settlement = oauth_client.settlements.get(SETTLEMENT_ID)
    first_chargebacks_page = settlement.chargebacks.list()
    assert first_chargebacks_page.has_previous() is False
    assert first_chargebacks_page.has_next() is True

    second_chargebacks_page = first_chargebacks_page.get_next()
    assert_list_object(second_chargebacks_page, Chargeback)

    subscription = next(second_chargebacks_page)
    assert subscription.id == "chb_n9z0tq"
