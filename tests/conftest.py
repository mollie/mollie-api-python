import json
import logging
import os
import time

import pytest
import responses

from mollie.api.client import Client

logger = logging.getLogger("mollie.pytest.fixtures")


@pytest.fixture
def client():
    """Setup a Mollie API client object."""
    api_key = os.environ.get("MOLLIE_API_KEY", "test_test")

    client = Client()
    client.set_api_key(api_key)
    return client


@pytest.fixture(scope="session")
def oauth_token():
    """Return a valid oauth token for resuming an existing OAuth client."""
    token = {
        "access_token": "access_H35x4awgfxPKPuHRjpKMAkP2bOgUs",
        "expires_in": 3600,
        "token_type": "bearer",
        "scope": [
            "profiles.read",
        ],
        "refresh_token": "refresh_asfqqJCxj9TjU8B544r44Tsu9bOgUs",
        "expires_at": time.time() + 300,  # token is valid for another 5 minutes
    }
    return token


@pytest.fixture
def oauth_client(oauth_token, response):
    """Setup a Mollie API client with initialized OAuth2 authentication."""
    client_id = "app_nvQQ4mGHqprcfFFqpnmbOgUs"
    client_secret = "2Tuc4qk8U6kCA8qBV3Fb2wwceDDfeRebDQpbOgUs"
    redirect_uri = "https://example.com/callback"
    scope = ("profiles.read",)

    def set_token(x):
        logger.info(f"Storing token: {x}")

    client = Client()
    client.setup_oauth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        token=oauth_token,
        set_token=set_token,
    )

    # Mock a forced token refresh, so we always have an authenticated client
    response.add(
        response.POST,
        "https://api.mollie.com/oauth2/tokens",
        body=json.dumps(oauth_token),
    )
    client._oauth_client.refresh_token(client.OAUTH_TOKEN_URL)

    return client


class ImprovedRequestsMock(responses.RequestsMock):
    """Wrapper adding a few shorthands to responses.RequestMock."""

    def get(self, url, filename, status=200, **kwargs):
        """Setup a mock response for a GET request."""
        body = self._get_body(filename)
        return self.add(responses.GET, url, body=body, status=status, content_type="application/hal+json", **kwargs)

    def post(self, url, filename, status=200, **kwargs):
        """Setup a mock response for a POST request."""
        body = self._get_body(filename)
        return self.add(responses.POST, url, body=body, status=status, content_type="application/hal+json", **kwargs)

    def delete(self, url, filename, status=204, **kwargs):
        """Setup a mock response for a DELETE request."""
        body = self._get_body(filename)
        return self.add(responses.DELETE, url, body=body, status=status, content_type="application/hal+json", **kwargs)

    def patch(self, url, filename, status=200, **kwargs):
        """Setup a mock response for a PATCH request."""
        body = self._get_body(filename)
        return self.add(responses.PATCH, url, body=body, status=status, content_type="application/hal+json", **kwargs)

    def _get_body(self, filename):
        """Read the response fixture file and return it."""
        file = os.path.join(os.path.dirname(__file__), "responses", f"{filename}.json")
        with open(file, encoding="utf-8") as f:
            return f.read()


@pytest.fixture
def response():
    """Setup the responses fixture."""
    with ImprovedRequestsMock() as mock:
        yield mock
