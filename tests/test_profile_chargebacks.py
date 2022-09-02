import re

import pytest

from mollie.api.error import RemovedIn215Warning
from mollie.api.objects.chargeback import Chargeback

from .utils import assert_list_object

PROFILE_ID = "pfl_v9hTwCvYqw"


def test_list_profile_chargebacks_by_profile_id(client, response):
    """Get chargebacks relevant to profile by profile id."""
    response.get(f"https://api.mollie.com/v2/chargebacks?profileId={PROFILE_ID}", "chargebacks_list")

    chargebacks = client.chargebacks.with_parent_id(PROFILE_ID).list()
    assert_list_object(chargebacks, Chargeback)


def test_list_profile_chargebacks_by_profile_object(client, response):
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")
    response.get(f"https://api.mollie.com/v2/chargebacks?profileId={PROFILE_ID}", "chargebacks_list")

    profile = client.profiles.get(PROFILE_ID)
    chargebacks = client.chargebacks.on(profile).list()
    assert_list_object(chargebacks, Chargeback)


def test_list_profile_chargebacks_by_deprecated_path_raises_warning(client, response):
    response.get(f"https://api.mollie.com/v2/chargebacks?profileId={PROFILE_ID}", "chargebacks_list")
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")

    with pytest.warns(
        RemovedIn215Warning,
        match=re.escape(
            "Using client.profile_chargebacks is deprecated, use "
            "client.chargebacks.with_parent_id(<profile_id>).list() to retrieve Profile chargebacks."
        ),
    ):
        client.profile_chargebacks.with_parent_id(PROFILE_ID).list()

    profile = client.profiles.get(PROFILE_ID)
    with pytest.warns(
        RemovedIn215Warning,
        match=re.escape(
            "Using client.profile_chargebacks is deprecated, use "
            "client.chargebacks.on(<profile_object>).list() to retrieve Profile chargebacks."
        ),
    ):
        client.profile_chargebacks.on(profile).list()
