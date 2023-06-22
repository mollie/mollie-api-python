from mollie.api.objects.capture import Capture

from .utils import assert_list_object

PAYMENT_ID = "tr_7UhSN1zuXS"
SETTLEMENT_ID = "stl_jDk30akdN"


def test_list_settlement_captures(oauth_client, response):
    """Get a list of captures relevant to settlement object."""
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}/captures", "settlement_captures_list")
    response.get(
        f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}/captures?limit=1&from=cpt_4qqhO89gsU",
        "settlement_captures_list_more",
    )

    settlement = oauth_client.settlements.get(SETTLEMENT_ID)
    captures = settlement.captures.list()
    assert_list_object(captures, Capture, 1)

    assert captures.has_next() is True
    more_captures = captures.get_next()
    assert_list_object(more_captures, Capture)
