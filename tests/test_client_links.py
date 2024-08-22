import pytest

from mollie.api.error import OpenBetaWarning, RequestSetupError
from mollie.api.objects.client_link import ClientLink

CLIENT_LINK_ID = "cl_vZCnNQsV2UtfXxYifWKWH"


def test_client_links_create(oauth_client, response):
    """
    Link a new or existing organization to your OAuth application, in effect creating a new client.
    The response contains a clientLink where you should redirect your customer to.
    """
    response.post("https://api.mollie.com/v2/client-links", "client_link_created")

    client_link = oauth_client.client_links.create(
        {
            "owner[email]": "info@example.org",
            "owner[givenName]": "Chuck",
            "owner[familyName]": "Norris",
            "address[country]": "NL",
            "name": "Mollie B.V.",
            "registrationNumber": 30204462,
            "vatNumber": "NL815839091B01",
        }
    )

    assert isinstance(client_link, ClientLink)
    assert client_link.id == CLIENT_LINK_ID
    assert client_link.get_object_name() == "client_links"
    assert client_link.resource == "client-link"
    assert client_link.link == "..."
    assert client_link.client_link == "https://my.mollie.com/dashboard/client-link/cl_vZCnNQsV2UtfXxYifWKWH"
    assert client_link.documentation_link == "..."


def test_client_links_create_requires_oauth_authorization(client):
    with pytest.raises(RequestSetupError, match="Creating client links requires OAuth authorization."):
        client.client_links.create({"irrelevant": "data"})


def test_client_links_open_beta_warning():
    with pytest.warns(
        OpenBetaWarning, match="ClientLink is currently in open beta, and the final specification may still change."
    ):
        ClientLink({}, None)
