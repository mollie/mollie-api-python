import pytest

from mollie.api.error import IdentifierError
from mollie.api.objects.profile import Profile
from mollie.api.resources.profiles import Profiles

from .utils import assert_list_object

PROFILE_ID = 'pfl_v9hTwCvYqw'


def test_profile_resource_class(oauth_client, response):
    response.get('https://api.mollie.com/v2/profiles/%s' % PROFILE_ID, 'profile_single')
    oauth_client.profiles.get(PROFILE_ID)

    assert isinstance(Profile.get_resource_class(oauth_client), Profiles)


def test_profiles_get_raises_identifier_error(oauth_client, response):
    response.get('https://api.mollie.com/v2/profiles/%s' % PROFILE_ID, 'profile_single')
    oauth_client.profiles.get(PROFILE_ID)

    with pytest.raises(IdentifierError):
        Profiles(oauth_client).get(None)


def test_create_profile(oauth_client, response):
    """Create a new profile."""
    response.post('https://api.mollie.com/v2/profiles', 'profile_new')

    profile = oauth_client.profiles.create({
      'name': 'My website name',
      'website': 'https://www.mywebsite.com',
      'email': 'info@mywebsite.com',
      'phone': '+31208202070',
      'categoryCode': '5399',
      'mode': 'live',
    })
    assert isinstance(profile, Profile)
    assert profile.id == PROFILE_ID


def test_update_profile(oauth_client, response):
    """Update an existing profile."""
    response.patch('https://api.mollie.com/v2/profiles/%s' % PROFILE_ID, 'profile_updated')

    updated_profile = oauth_client.profiles.update(PROFILE_ID, {
        'name': 'My website name updated',
        'email': 'updated-profile@example.org',
    })
    assert isinstance(updated_profile, Profile)
    assert updated_profile.name == 'My website name updated'
    assert updated_profile.email == 'updated-profile@example.org'


def test_delete_profile(oauth_client, response):
    """Delete a profile."""
    response.delete('https://api.mollie.com/v2/profiles/%s' % PROFILE_ID, 'empty')

    deleted_profile = oauth_client.profiles.delete('pfl_v9hTwCvYqw')
    assert deleted_profile == {}


def test_list_profiles(oauth_client, response):
    """Retrieve a list of existing profiles."""
    response.get('https://api.mollie.com/v2/profiles', 'profiles_list')

    profiles = oauth_client.profiles.list()
    assert_list_object(profiles, Profile)


def test_get_profile(oauth_client, response):
    """Retrieve a single profile."""
    response.get('https://api.mollie.com/v2/profiles/%s' % PROFILE_ID, 'profile_single')
    response.get('https://api.mollie.com/v2/chargebacks?profileId=%s' % PROFILE_ID, 'chargebacks_list')
    response.get('https://api.mollie.com/v2/methods?profileId=%s' % PROFILE_ID, 'methods_list')
    response.get('https://api.mollie.com/v2/payments?profileId=%s' % PROFILE_ID, 'payments_list')
    response.get('https://api.mollie.com/v2/refunds?profileId=%s' % PROFILE_ID, 'refunds_list')

    profile = oauth_client.profiles.get(PROFILE_ID)
    chargebacks = oauth_client.profile_chargebacks.with_parent_id(PROFILE_ID).list()
    methods = oauth_client.profile_methods.with_parent_id(PROFILE_ID).list()
    payments = oauth_client.profile_payments.with_parent_id(PROFILE_ID).list()
    refunds = oauth_client.profile_refunds.with_parent_id(PROFILE_ID).list()

    assert isinstance(profile, Profile)
    assert profile.id == PROFILE_ID
    assert profile.name == 'My website name'
    assert profile.email == 'info@mywebsite.com'
    assert profile.mode == 'live'
    assert profile.resource == 'profile'
    assert profile.created_at == '2018-03-20T09:28:37+00:00'
    assert profile.website == 'https://www.mywebsite.com'
    assert profile.phone == '+31208202070'
    assert profile.category_code == 5399
    assert profile.status == 'verified'
    assert profile.review == {"status": "pending"}
    assert profile.checkout_preview_url == 'https://www.mollie.com/payscreen/preview/pfl_v9hTwCvYqw'
    assert profile.chargebacks == chargebacks
    assert profile.methods == methods
    assert profile.payments == payments
    assert profile.refunds == refunds
    assert profile.is_unverified() is False
    assert profile.is_verified() is True
    assert profile.is_blocked() is False


def test_profile_enable_payment_method(oauth_client, response):
    response.get('https://api.mollie.com/v2/profiles/%s' % PROFILE_ID, 'profile_new')
    response.post(
        'https://api.mollie.com/v2/profiles/%s/methods/%s' % (PROFILE_ID, 'bancontact'),
        'profile_enable_payment_method'
    )

    profile = oauth_client.profiles.get(PROFILE_ID)
    method = oauth_client.profile_methods.on(profile, 'bancontact').create()
    assert method.id == 'bancontact'


def test_profile_disable_payment_method(oauth_client, response):
    response.get('https://api.mollie.com/v2/profiles/%s' % PROFILE_ID, 'profile_new')
    response.delete('https://api.mollie.com/v2/profiles/%s/methods/%s' % (PROFILE_ID, 'bancontact'), 'empty', 204)

    profile = oauth_client.profiles.get(PROFILE_ID)
    method = oauth_client.profile_methods.on(profile, 'bancontact').delete()
    assert method == {}
