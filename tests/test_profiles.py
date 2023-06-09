import pytest

from mollie.api.error import APIDeprecationWarning, IdentifierError
from mollie.api.objects.profile import Profile
from mollie.api.resources import ProfileChargebacks, ProfileMethods, ProfilePayments, ProfileRefunds

from .utils import assert_list_object

PROFILE_ID = "pfl_v9hTwCvYqw"


def test_create_profile(oauth_client, response):
    """Create a new profile."""
    response.post("https://api.mollie.com/v2/profiles", "profile_single")

    profile = oauth_client.profiles.create(
        {
            "name": "My website name",
            "website": "https://www.mywebsite.com",
            "email": "info@mywebsite.com",
            "phone": "+31208202070",
            "businessCategory": "AMUSEMENT_PARKS",
            "mode": "live",
        }
    )
    assert isinstance(profile, Profile)
    assert profile.id == PROFILE_ID


def test_update_profile(oauth_client, response):
    """Update an existing profile."""
    response.patch(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_updated")

    updated_profile = oauth_client.profiles.update(
        PROFILE_ID,
        {
            "name": "My website name updated",
            "email": "updated-profile@example.org",
        },
    )
    assert isinstance(updated_profile, Profile)
    assert updated_profile.name == "My website name updated"
    assert updated_profile.email == "updated-profile@example.org"


def test_update_profile_invalid_id(oauth_client, response):
    data = {}
    with pytest.raises(IdentifierError) as excinfo:
        oauth_client.profiles.update("invalid", data)
    assert str(excinfo.value) == "Invalid profile ID 'invalid', it should start with 'pfl_'."


def test_delete_profile(oauth_client, response):
    """Delete a profile."""
    response.delete(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "empty")

    deleted_profile = oauth_client.profiles.delete("pfl_v9hTwCvYqw")
    assert deleted_profile == {}


def test_delete_profile_invalid_id(oauth_client, response):
    with pytest.raises(IdentifierError) as excinfo:
        oauth_client.profiles.delete("invalid")
    assert str(excinfo.value) == "Invalid profile ID 'invalid', it should start with 'pfl_'."


def test_list_profiles(oauth_client, response):
    """Retrieve a list of existing profiles."""
    response.get("https://api.mollie.com/v2/profiles", "profiles_list")

    profiles = oauth_client.profiles.list()
    assert_list_object(profiles, Profile)


def test_get_profile(oauth_client, response):
    """Retrieve a single profile."""
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")

    profile = oauth_client.profiles.get(PROFILE_ID)

    assert isinstance(profile, Profile)
    assert profile.id == PROFILE_ID
    assert profile.name == "My website name"
    assert profile.email == "info@mywebsite.com"
    assert profile.mode == "live"
    assert profile.resource == "profile"
    assert profile.created_at == "2018-03-20T09:28:37+00:00"
    assert profile.website == "https://www.mywebsite.com"
    assert profile.phone == "+31208202070"
    assert profile.business_category == "AMUSEMENT_PARKS"
    assert profile.status == "verified"
    assert profile.review == {"status": "pending"}
    assert profile.checkout_preview_url == "https://www.mollie.com/payscreen/preview/pfl_v9hTwCvYqw"
    assert isinstance(profile.chargebacks, ProfileChargebacks)
    assert isinstance(profile.methods, ProfileMethods)
    assert isinstance(profile.payments, ProfilePayments)
    assert isinstance(profile.refunds, ProfileRefunds)
    assert profile.is_unverified() is False
    assert profile.is_verified() is True
    assert profile.is_blocked() is False


def test_get_profile_invalid_id(oauth_client, response):
    with pytest.raises(IdentifierError) as excinfo:
        oauth_client.profiles.get("invalid")
    assert str(excinfo.value) == "Invalid profile ID 'invalid', it should start with 'pfl_'."


def test_get_current_profile(oauth_client, response):
    response.get("https://api.mollie.com/v2/profiles/me", "profile_single")

    profile = oauth_client.profiles.get("me")
    assert isinstance(profile, Profile)


def test_profile_category_code_is_deprecated(client, response):
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")

    profile = client.profiles.get(PROFILE_ID)
    with pytest.warns(APIDeprecationWarning, match="Using categoryCode is deprecated"):
        assert profile.category_code == 5399
