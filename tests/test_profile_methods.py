from mollie.api.objects.method import Method

from .utils import assert_list_object

PROFILE_ID = 'pfl_v9hTwCvYqw'


def test_get_profile_methods_by_profile_id(client, response):
    """Get methods relevant to profile by profile id."""
    response.get('https://api.mollie.com/v2/methods?profileId=%s' % PROFILE_ID, 'methods_list')

    methods = client.profile_methods.with_parent_id(PROFILE_ID).list()
    assert_list_object(methods, Method)
