from mollie.api.objects.payment import Payment

from .utils import assert_list_object

PROFILE_ID = "pfl_v9hTwCvYqw"


def test_get_profile_payments(oauth_client, response):
    """Get payments relevant to profile by profile id."""
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")
    response.get(f"https://api.mollie.com/v2/payments?profileId={PROFILE_ID}", "payments_list")

    profile = oauth_client.profiles.get(PROFILE_ID)
    payments = profile.payments.list()
    assert_list_object(payments, Payment)
