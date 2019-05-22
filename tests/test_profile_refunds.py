from mollie.api.objects.refund import Refund

from .utils import assert_list_object

PROFILE_ID = 'pfl_v9hTwCvYqw'


def test_get_profile_refunds_by_profile_id(client, response):
    """Get refunds relevant to profile by profile id."""
    response.get('https://api.mollie.com/v2/refunds?profileId=%s' % PROFILE_ID, 'refunds_list')

    refunds = client.profile_refunds.with_parent_id(PROFILE_ID).list()
    assert_list_object(refunds, Refund)
