import pytest

from mollie.api.error import IdentifierError
from mollie.api.objects.organization import Organization

ORGANIZATION_ID = "org_12345678"


def test_get_organization(oauth_client, response):
    """Retrieve a single organization."""
    response.get(f"https://api.mollie.com/v2/organizations/{ORGANIZATION_ID}", "organization_single")

    organization = oauth_client.organizations.get(ORGANIZATION_ID)
    assert isinstance(organization, Organization)
    assert organization.id == ORGANIZATION_ID
    assert organization.resource == "organization"
    assert organization.name == "Mollie B.V."
    assert organization.email == "info@mollie.com"
    assert organization.locale == "nl_NL"
    assert organization.vat_number == "NL815839091B01"
    assert organization.vat_regulation == "dutch"
    assert organization.registration_number == "30204462"
    assert organization.address == {
        "city": "Amsterdam",
        "country": "NL",
        "postalCode": "1016 EE",
        "streetAndNumber": "Keizersgracht 313",
    }


def test_get_current_organization(oauth_client, response):
    """Retrieve a current organization."""
    response.get("https://api.mollie.com/v2/organizations/me", "organization_current")

    organization = oauth_client.organizations.get("me")
    assert isinstance(organization, Organization)
    assert organization.id == ORGANIZATION_ID
    assert organization.name == "Mollie B.V."
    assert organization.email == "info@mollie.com"
    assert organization.locale == "nl_NL"
    assert organization.vat_number == "NL815839091B01"
    assert organization.vat_regulation == "dutch"
    assert organization.registration_number == "30204462"
    assert organization.address == {
        "city": "Amsterdam",
        "country": "NL",
        "postalCode": "1016 EE",
        "streetAndNumber": "Keizersgracht 313",
    }
    assert organization.dashboard == "https://mollie.com/dashboard/org_12345678"


def test_get_organization_invalid_id(oauth_client):
    with pytest.raises(IdentifierError) as excinfo:
        oauth_client.organizations.get("invalid")
    assert str(excinfo.value) == "Invalid organization ID 'invalid', it should start with 'org_'."
