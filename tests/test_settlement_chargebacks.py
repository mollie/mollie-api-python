import re

import pytest

from mollie.api.error import RemovedIn215Warning
from mollie.api.objects.chargeback import Chargeback

from .utils import assert_list_object

PAYMENT_ID = "tr_7UhSN1zuXS"
SETTLEMENT_ID = "stl_jDk30akdN"
CHARGEBACK_ID = "chb_n9z0tp"


def test_list_settlement_chargebacks_by_chargeback_id(oauth_client, response):
    """Get chargebacks relevant to settlement by settlement id."""
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}/chargebacks", "chargebacks_list")

    chargebacks = oauth_client.chargebacks.with_parent_id(SETTLEMENT_ID).list()
    assert_list_object(chargebacks, Chargeback)


def test_list_settlement_chargebacks_by_settlement_object(oauth_client, response):
    """Get a list of chargebacks relevant to settlement object."""
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}/chargebacks", "chargebacks_list")
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")

    settlement = oauth_client.settlements.get(SETTLEMENT_ID)
    chargebacks = oauth_client.chargebacks.on(settlement).list()
    assert_list_object(chargebacks, Chargeback)


def test_list_settlement_chargebacks_by_deprecated_path_raises_warning(oauth_client, response):
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}/chargebacks", "chargebacks_list")
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")

    with pytest.warns(
        RemovedIn215Warning,
        match=re.escape(
            "Using client.settlement_chargebacks is deprecated, use "
            "client.chargebacks.with_parent_id(<settlement_id>).list() to retrieve Settlement chargebacks."
        ),
    ):
        oauth_client.settlement_chargebacks.with_parent_id(SETTLEMENT_ID).list()

    settlement = oauth_client.settlements.get(SETTLEMENT_ID)
    with pytest.warns(
        RemovedIn215Warning,
        match=re.escape(
            "Using client.settlement_chargebacks is deprecated, use "
            "client.chargebacks.on(<settlement_object>).list() to retrieve Settlement chargebacks."
        ),
    ):
        oauth_client.settlement_chargebacks.on(settlement).list()
