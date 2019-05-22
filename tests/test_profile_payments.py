from mollie.api.objects.payment import Payment

from .utils import assert_list_object

PROFILE_ID = 'pfl_v9hTwCvYqw'


def test_get_profile_payments_by_profile_id(client, response):
    """Get payments relevant to profile by profile id."""
    response.get('https://api.mollie.com/v2/payments?profileId=%s' % PROFILE_ID, 'payments_list')

    payments = client.profile_payments.with_parent_id(PROFILE_ID).list()
    assert_list_object(payments, Payment)
