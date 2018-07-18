import os

import pytest
import Mollie
import responses


@pytest.fixture(scope='session')
def client():
    """Setup a Mollie API client object."""
    api_key = os.environ.get('MOLLIE_API_KEY', 'test_test')

    client = Mollie.API.Client()
    client.setApiKey(api_key)
    return client


class ImprovedRequestsMock(responses.RequestsMock):
    """Wrapper adding a few shorthands to responses.RequestMock."""

    def get(self, url, filename, status=200):
        """Setup a mock response for a GET request."""
        file = os.path.join(os.path.dirname(__file__), 'responses', '%s.json' % filename)
        body = open(file).read()
        self.add(responses.GET, url, body=body, status=status)

    def post(self, url, filename, status=200):
        """Setup a mock response for a GET request."""
        file = os.path.join(os.path.dirname(__file__), 'responses', '%s.json' % filename)
        body = open(file).read()
        self.add(responses.POST, url, body=body, status=status)


@pytest.fixture
def response():
    """Setup the responses fixture."""
    with ImprovedRequestsMock() as mock:
        yield mock
