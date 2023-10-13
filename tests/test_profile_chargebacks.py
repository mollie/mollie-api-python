from responses import matchers

from mollie.api.objects.chargeback import Chargeback

from .utils import assert_list_object

PROFILE_ID = "pfl_v9hTwCvYqw"


def test_get_profile_chargebacks(oauth_client, response):
    """Get chargebacks relevant to profile by profile id."""
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")
    response.get(
        "https://api.mollie.com/v2/chargebacks",
        "profile_chargebacks_list",
        match=[matchers.query_string_matcher(f"profileId={PROFILE_ID}")],
    )

    profile = oauth_client.profiles.get(PROFILE_ID)
    chargebacks = profile.chargebacks.list()
    assert_list_object(chargebacks, Chargeback)


def test_list_profile_chargebacks_pagination(oauth_client, response):
    """Retrieve a list of paginated profile chargebacks."""
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")
    response.get(
        "https://api.mollie.com/v2/chargebacks",
        "profile_chargebacks_list",
        match=[matchers.query_string_matcher(f"profileId={PROFILE_ID}")],
    )
    response.get(
        "https://api.mollie.com/v2/chargebacks",
        "profile_chargebacks_list_more",
        match=[matchers.query_string_matcher(f"profileId={PROFILE_ID}&from=chb_n9z0tq")],
    )

    profile = oauth_client.profiles.get(PROFILE_ID)
    first_chargebacks_page = profile.chargebacks.list()
    assert first_chargebacks_page.has_previous() is False
    assert first_chargebacks_page.has_next() is True

    second_chargebacks_page = first_chargebacks_page.get_next()
    assert_list_object(second_chargebacks_page, Chargeback)

    subscription = next(second_chargebacks_page)
    assert subscription.id == "chb_n9z0tq"
