from mollie.api.objects.chargeback import Chargeback

from .utils import assert_list_object

PROFILE_ID = "pfl_v9hTwCvYqw"


def test_list_profile_chargebacks(oauth_client, response):
    """Get chargebacks relevant to profile by profile id."""
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")
    response.get(f"https://api.mollie.com/v2/chargebacks?profileId={PROFILE_ID}", "profile_chargebacks_list")
    response.get(
        f"https://api.mollie.com/v2/chargebacks?profileId={PROFILE_ID}&limit=1&from=chb_n9z0tq",
        "profile_chargebacks_list_more",
    )

    profile = oauth_client.profiles.get(PROFILE_ID)
    chargebacks = profile.chargebacks.list()
    assert_list_object(chargebacks, Chargeback)

    assert chargebacks.has_next()
    more_chargebacks = chargebacks.get_next()
    assert_list_object(more_chargebacks, Chargeback)
