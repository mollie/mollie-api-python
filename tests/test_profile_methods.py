import json

import pytest

from mollie.api.error import IdentifierError
from mollie.api.objects.issuer import Issuer
from mollie.api.objects.method import Method

from .utils import assert_empty_object, assert_list_object

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
def test_enable_profile_payment_method_issuer_error(oauth_client, response, method_id):
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")

    profile = oauth_client.profiles.get(PROFILE_ID)
    with pytest.raises(IdentifierError) as excinfo:
        profile.methods.enable(method_id)
    assert str(excinfo.value) == f"Cannot enable '{method_id}' method, it requires enabling specific issuers."


def test_profile_disable_payment_method(oauth_client, response):
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")
    response.delete(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}/methods/{METHOD_ID}", "empty", 204)

    profile = oauth_client.profiles.get(PROFILE_ID)
    method = profile.methods.disable(METHOD_ID)
    assert_empty_object(method, Method)


@pytest.mark.parametrize("method_id", ["voucher", "giftcard"])
def test_disable_profile_payment_method_issuer_error(oauth_client, response, method_id):
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")

    profile = oauth_client.profiles.get(PROFILE_ID)
    with pytest.raises(IdentifierError) as excinfo:
        profile.methods.disable(method_id)
    assert str(excinfo.value) == f"Cannot disable '{method_id}' method, it requires disabling specific issuers."


def test_list_profile_payment_methods(oauth_client, response):
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")
    response.get(f"https://api.mollie.com/v2/methods?profileId={PROFILE_ID}", "methods_list")

    profile = oauth_client.profiles.get(PROFILE_ID)
    methods = profile.methods.list()
    assert_list_object(methods, Method)


def test_profile_payment_method_enable_issuer(oauth_client, response):
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")
    response.post(
        f"https://api.mollie.com/v2/profiles/{PROFILE_ID}/methods/giftcard/issuers/{GIFTCARD_ISSUER_ID}",
        "issuer_giftcard",
    )

    profile = oauth_client.profiles.get(PROFILE_ID)
    issuer = profile.methods.enable_issuer("giftcard", GIFTCARD_ISSUER_ID)
    assert isinstance(issuer, Issuer)
    assert issuer.id == GIFTCARD_ISSUER_ID


def test_profile_payment_method_enable_issuer_with_payload(oauth_client, response):
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")
    response.post(
        f"https://api.mollie.com/v2/profiles/{PROFILE_ID}/methods/voucher/issuers/{VOUCHER_ISSUER_ID}",
        "issuer_voucher",
    )

    profile = oauth_client.profiles.get(PROFILE_ID)
    issuer = profile.methods.enable_issuer("voucher", VOUCHER_ISSUER_ID, {"contractId": "abc123"})
    assert isinstance(issuer, Issuer)
    assert issuer.id == VOUCHER_ISSUER_ID

    # Inspect the request that was sent
    request = response.calls[-1].request
    assert (
        request.url == f"https://api.mollie.com/v2/profiles/{PROFILE_ID}/methods/voucher/issuers/{VOUCHER_ISSUER_ID}"
    )
    assert json.loads(request.body) == {"contractId": "abc123"}


def test_profile_payment_method_enable_issuer_invalid_method(oauth_client, response):
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")

    profile = oauth_client.profiles.get(PROFILE_ID)
    with pytest.raises(IdentifierError) as excinfo:
        profile.methods.enable_issuer("bancontact", GIFTCARD_ISSUER_ID)
    assert str(excinfo.value) == "Payment method 'bancontact' does not support issuers."


def test_profile_payment_method_disable_issuer(oauth_client, response):
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")
    response.delete(
        f"https://api.mollie.com/v2/profiles/{PROFILE_ID}/methods/giftcard/issuers/{GIFTCARD_ISSUER_ID}",
        "empty",
        status=204,
    )

    profile = oauth_client.profiles.get(PROFILE_ID)
    issuer = profile.methods.disable_issuer("giftcard", GIFTCARD_ISSUER_ID)
    assert_empty_object(issuer, Issuer)


def test_profile_payment_method_disable_issuer_invalid_method(oauth_client, response):
    response.get(f"https://api.mollie.com/v2/profiles/{PROFILE_ID}", "profile_single")

    profile = oauth_client.profiles.get(PROFILE_ID)
    with pytest.raises(IdentifierError) as excinfo:
        profile.methods.disable_issuer("bancontact", GIFTCARD_ISSUER_ID)
    assert str(excinfo.value) == "Payment method 'bancontact' does not support issuers."
