import pkg_resources
import pytest

from mollie.api.client import Client, generate_querystring
from mollie.api.error import *  # noqa


@pytest.mark.parametrize('params, querystring', [
    ({}, None),
    ({'locale': 'nl_NL'}, 'locale=nl_NL'),
    ({'locale': 'nl_NL', 'hoeba': 'kek'}, 'hoeba=kek&locale=nl_NL'),
    ({'amount': {'value': '100.00', 'currency': 'USD'}}, 'amount%5Bcurrency%5D=USD&amount%5Bvalue%5D=100.00')
])
def test_generate_querystring(params, querystring):
    """Verify that we can generate querystring that are correctly quoted."""
    result = generate_querystring(params)
    assert result == querystring


def test_client_querystring(client, response):
    """Verify that we are triggering the correct URL when using querystring with square brackets."""
    response.add(
        response.GET,
        'https://api.mollie.com/v2/methods?amount[currency]=USD&amount[value]=100.00',
        body=response._get_body('methods_multiple'),
        match_querystring=True
    )

    params = {'amount': {'currency': 'USD', 'value': '100.00'}}
    methods = client.methods.all(**params)
    assert methods.count == 11


def test_client_no_api_key():
    """A Request without an API key should raise an error."""
    client = Client()
    with pytest.raises(RequestSetupError) as excinfo:
        client.customers.all()
    assert excinfo.match('You have not set an API key.')


def test_client_invalid_api_key():
    """Setting up an invalid api key raises an error."""
    client = Client()
    with pytest.raises(RequestSetupError) as excinfo:
        client.set_api_key('invalid')
    assert excinfo.match('Invalid API key: "invalid"')


def test_client_no_cert_bundle(monkeypatch):
    """A request should raise an error when the certificate bundle is not available."""
    def mockreturn(modulepath, file):
        return ''
    monkeypatch.setattr(pkg_resources, 'resource_filename', mockreturn)

    client = Client()
    client.set_api_key('test_test')
    with pytest.raises(RequestSetupError) as excinfo:
        client.customers.all()
    assert excinfo.match('Unable to load cacert.pem')


def test_client_request_error(client, response):
    """
    When the remote server refuses connections, an error should be raised.

    The 'response' fixture blocks all outgoing connections, also when no actual responses are configured.
    """
    client.set_api_endpoint('https://api.mollie.invalid/')
    with pytest.raises(RequestError) as excinfo:
        client.customers.all()
    assert excinfo.match('Unable to communicate with Mollie: Connection refused')
