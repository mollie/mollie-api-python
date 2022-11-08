import pytest

from mollie.api.error import IdentifierError
from mollie.api.objects.client import Client
from mollie.api.objects.onboarding import Onboarding
from mollie.api.objects.organization import Organization

from .utils import assert_list_object

CLIENT_ID = "org_1337"


def test_list_clients(oauth_client, response):
    """Retrieve a list of clients related to the authenticated partner account."""
    response.get("https://api.mollie.com/v2/clients", "clients_list")

    clients = oauth_client.clients.list()
    assert_list_object(clients, Client)


def test_get_client(oauth_client, response):
    """Retrieve a single client, linked to your partner account, by its ID."""
    response.get(f"https://api.mollie.com/v2/clients/{CLIENT_ID}", "client_single")

    client = oauth_client.clients.get(CLIENT_ID)
    assert isinstance(client, Client)
    assert client.id == CLIENT_ID
    assert client.resource == "client"
    assert client.organisation_created_at == "2018-03-21T13:13:37+00:00"


def test_get_client_invalid_id(oauth_client):
    with pytest.raises(IdentifierError) as excinfo:
        oauth_client.clients.get("invalid")
    assert str(excinfo.value) == "Invalid client ID 'invalid', it should start with 'org_'."


def test_client_get_organization(oauth_client, response):
    response.get(f"https://api.mollie.com/v2/clients/{CLIENT_ID}", "client_single")
    response.get(f"https://api.mollie.com/v2/organizations/{CLIENT_ID}", "organization_single")

    client = oauth_client.clients.get(CLIENT_ID)
    organization = client.get_organization()
    assert isinstance(organization, Organization)


def test_client_get_onboarding(oauth_client, response):
    response.get(f"https://api.mollie.com/v2/clients/{CLIENT_ID}", "client_single")
    response.get(f"https://api.mollie.com/v2/onboarding/{CLIENT_ID}", "onboarding_single")

    client = oauth_client.clients.get(CLIENT_ID)
    onboarding = client.get_onboarding()
    assert isinstance(onboarding, Onboarding)
