import re

import pytest

from mollie.api.error import RemovedIn215Warning
from mollie.api.objects.capture import Capture

from .utils import assert_list_object

PAYMENT_ID = "tr_7UhSN1zuXS"
SETTLEMENT_ID = "stl_jDk30akdN"


def test_list_settlement_captures_by_parent_id(oauth_client, response):
    """Get captures relevant to settlement by settlement id."""
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}/captures", "captures_list")

    captures = oauth_client.captures.with_parent_id(SETTLEMENT_ID).list()
    assert_list_object(captures, Capture)


def test_list_settlement_captures_by_parent_object(oauth_client, response):
    """Get a list of captures relevant to a settlement object."""
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}/captures", "captures_list")
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")

    settlement = oauth_client.settlements.get(SETTLEMENT_ID)
    captures = oauth_client.captures.on(settlement).list()
    assert_list_object(captures, Capture)


def test_list_settlement_captures_through_deprecated_path_raises_warning(oauth_client, response):
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}/captures", "captures_list")
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")

    with pytest.warns(
        RemovedIn215Warning,
        match=re.escape(
            "Using client.settlement_captures is deprecated, use "
            "client.captures.with_parent_id(<settlement_id>).list() to retrieve Settlement captures."
        ),
    ):
        oauth_client.settlement_captures.with_parent_id(SETTLEMENT_ID).list()

    settlement = oauth_client.settlements.get(SETTLEMENT_ID)
    with pytest.warns(
        RemovedIn215Warning,
        match=re.escape(
            "Using client.settlement_captures is deprecated, use "
            "client.captures.on(<settlement_object>).list() to retrieve Settlement captures."
        ),
    ):
        oauth_client.settlement_captures.on(settlement).list()
