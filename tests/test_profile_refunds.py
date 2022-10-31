from mollie.api.objects.refund import Refund

from .utils import assert_list_object

PROFILE_ID = "pfl_v9hTwCvYqw"


def test_get_profile_refunds(oauth_client, response):
    """Get refunds relevant to profile."""
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")
    response.get(f"https://api.mollie.com/v2/refunds?profileId={PROFILE_ID}", "refunds_list")

    profile = oauth_client.profiles.get(PROFILE_ID)
    refunds = profile.refunds.list()
    assert_list_object(refunds, Refund)
