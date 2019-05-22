from mollie.api.objects.chargeback import Chargeback

from .utils import assert_list_object

PROFILE_ID = 'pfl_v9hTwCvYqw'


def test_get_profile_chargebacks_by_profile_id(client, response):
    """Get chargebacks relevant to profile by profile id."""
    response.get('https://api.mollie.com/v2/chargebacks?profileId=%s' % PROFILE_ID, 'chargebacks_list')

    chargebacks = client.profile_chargebacks.with_parent_id(PROFILE_ID).list()
    assert_list_object(chargebacks, Chargeback)
