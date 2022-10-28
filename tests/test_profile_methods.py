import pytest

from mollie.api.error import IdentifierError
from mollie.api.objects.method import Method

from .utils import assert_list_object

PROFILE_ID = "pfl_v9hTwCvYqw"
METHOD_ID = "bancontact"
GIFTCARD_ISSUER_ID = "festivalcadeau"
VOUCHER_ISSUER_ID = "appetiz"


def test_enable_profile_payment_method(oauth_client, response):
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")
    response.post(
        f"https://api.mollie.com/v2/profiles/{PROFILE_ID}/methods/{METHOD_ID}",
        "profile_enable_payment_method",
    )

    profile = oauth_client.profiles.get(PROFILE_ID)
    method = profile.methods.enable(METHOD_ID)
    assert method.id == METHOD_ID


@pytest.mark.parametrize("method_id", ["voucher", "giftcard"])
def test_enable_profile_payment_method_issuer_missing(oauth_client, response, method_id):
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")

    profile = oauth_client.profiles.get(PROFILE_ID)
    with pytest.raises(IdentifierError) as excinfo:
        profile.methods.enable(method_id)
    assert str(excinfo.value) == f"Cannot enable '{method_id}' method, no issuer specified."


def test_profile_disable_payment_method(oauth_client, response):
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")
    response.delete(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}/methods/{METHOD_ID}", "empty", 204)

    profile = oauth_client.profiles.get(PROFILE_ID)
    method = profile.methods.disable(METHOD_ID)
    assert method == {}


@pytest.mark.parametrize("method_id", ["voucher", "giftcard"])
def test_disable_profile_payment_method_issuer_missing(oauth_client, response, method_id):
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")

    profile = oauth_client.profiles.get(PROFILE_ID)
    with pytest.raises(IdentifierError) as excinfo:
        profile.methods.disable(method_id)
    assert str(excinfo.value) == f"Cannot disable '{method_id}' method, no issuer specified."


def test_list_profile_payment_methods(oauth_client, response):
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")
    response.get(f"https://api.mollie.com/v2/methods?profileId={PROFILE_ID}", "methods_list")

    profile = oauth_client.profiles.get(PROFILE_ID)
    methods = profile.methods.list()
    assert_list_object(methods, Method)
