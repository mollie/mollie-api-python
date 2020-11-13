import logging
import os
import time

import pytest
import responses

from mollie.api.client import Client

logger = logging.getLogger('mollie.pytest.fixtures')


@pytest.fixture(scope='session')
def client():
    """Setup a Mollie API client object."""
    api_key = os.environ.get('MOLLIE_API_KEY', 'test_test')

    client = Client()
    client.set_api_key(api_key)
    return client


@pytest.fixture(scope='session')
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
        "expires_at": time.time() + 300  # token is valid for another 5 minutes
    }
    return token


@pytest.fixture(scope='session')
def oauth_client(oauth_token):
    """Setup a Mollie API client with initialized OAuth2 authentication."""
    client_id = "app_nvQQ4mGHqprcfFFqpnmbOgUs"
    client_secret = "2Tuc4qk8U6kCA8qBV3Fb2wwceDDfeRebDQpbOgUs"
    redirect_uri = "https://example.com/callback"
    scope = ("organizations.read",)

    def set_token(x):
        logger.info("Storing token: %s", x)

    client = Client()
    client.setup_oauth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        token=oauth_token,
        set_token=set_token,
    )
    assert client._oauth_client.authorized is True
    return client


class ImprovedRequestsMock(responses.RequestsMock):
    """Wrapper adding a few shorthands to responses.RequestMock."""

    def get(self, url, filename, status=200):
        """Setup a mock response for a GET request."""
        body = self._get_body(filename)
        self.add(responses.GET, url, body=body, status=status, content_type='application/hal+json')

    def post(self, url, filename, status=200):
        """Setup a mock response for a POST request."""
        body = self._get_body(filename)
        self.add(responses.POST, url, body=body, status=status, content_type='application/hal+json')

    def delete(self, url, filename, status=204):
        """Setup a mock response for a DELETE request."""
        body = self._get_body(filename)
        self.add(responses.DELETE, url, body=body, status=status, content_type='application/hal+json')

    def patch(self, url, filename, status=200):
        """Setup a mock response for a PATCH request."""
        body = self._get_body(filename)
        self.add(responses.PATCH, url, body=body, status=status, content_type='application/hal+json')

    def _get_body(self, filename):
        """Read the response fixture file and return it."""
        file = os.path.join(os.path.dirname(__file__), 'responses', '%s.json' % filename)
        return open(file).read()


@pytest.fixture
def response():
    """Setup the responses fixture."""
    with ImprovedRequestsMock() as mock:
        yield mock
