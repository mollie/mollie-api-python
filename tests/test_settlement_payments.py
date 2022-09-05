import re

import pytest

from mollie.api.error import RemovedIn215Warning
from mollie.api.objects.payment import Payment

from .utils import assert_list_object

SETTLEMENT_ID = "stl_jDk30akdN"


def test_list_customer_payments(oauth_client, response):
    """Retrieve a list of payments related to a settlement id."""
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}/payments", "settlement_payments_multiple")

    payments = oauth_client.payments.with_parent_id(SETTLEMENT_ID).list()
    assert_list_object(payments, Payment)


def test_list_customer_payments_through_deprecated_path_raises_warnings(oauth_client, response):
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}/payments", "settlement_payments_multiple")
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")

    with pytest.warns(
        RemovedIn215Warning,
        match=re.escape(
            "Using client.settlement_payments is deprecated, use "
            "client.payments.with_parent_id(<settlement_id>).list() to retrieve Settlement payments."
        ),
    ):
        oauth_client.settlement_payments.with_parent_id(SETTLEMENT_ID).list()

    settlement = oauth_client.settlements.get(SETTLEMENT_ID)
    with pytest.warns(
        RemovedIn215Warning,
        match=re.escape(
            "Using client.settlement_payments is deprecated, use "
            "client.payments.with_parent_id(<settlement_id>).list() to retrieve Settlement payments."
        ),
    ):
        oauth_client.settlement_payments.on(settlement).list()
