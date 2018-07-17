import os

import pytest
import Mollie


@pytest.fixture(scope='session')
def client():
    """Setup a Mollie API client object."""
    api_key = os.environ.get('MOLLIE_API_KEY', '')

    client = Mollie.API.Client()
    client.setApiKey(api_key)
    return client
