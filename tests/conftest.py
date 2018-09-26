import os

import pytest
import responses

from mollie.api.client import Client


@pytest.fixture(scope='session')
def client():
    """Setup a Mollie API client object."""
    api_key = os.environ.get('MOLLIE_API_KEY', 'test_test')

    client = Client()
    client.set_api_key(api_key)
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
