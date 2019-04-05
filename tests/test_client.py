# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import sys
from datetime import datetime

import mock
import pytest
import requests.adapters

from mollie.api.client import Client, generate_querystring
from mollie.api.error import (
    DataConsistencyError,
    IdentifierError,
    NotFoundError,
    RequestError,
    RequestSetupError,
    ResponseError,
    ResponseHandlingError,
    UnauthorizedError,
    UnprocessableEntityError,
)


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
        body=response._get_body('methods_list'),
        match_querystring=True
    )

    params = {'amount': {'currency': 'USD', 'value': '100.00'}}
    methods = client.methods.list(**params)
    assert methods.count == 11


def test_client_api_key():
    """Setting up a valid api key or access token should be possible."""
    client = Client()

    client.set_access_token('access_123')
    assert client.api_key == 'access_123'

    client.set_api_key('live_123')
    assert client.api_key == 'live_123'

    client.set_api_key('test_123')
    assert client.api_key == 'test_123'


def test_client_no_api_key():
    """A Request without an API key should raise an error."""
    client = Client()
    with pytest.raises(RequestSetupError, match='You have not set an API key.'):
        client.customers.list()


def test_client_invalid_api_key():
    """Setting up an invalid api key raises an error."""
    client = Client()

    with pytest.raises(RequestSetupError, match="Invalid API key: 'invalid'"):
        client.set_api_key('invalid')

    with pytest.raises(RequestSetupError, match="Invalid API key: 'access_123'"):
        client.set_api_key('access_123')

    with pytest.raises(RequestSetupError, match="Invalid access token: 'invalid'"):
        client.set_access_token('invalid')

    with pytest.raises(RequestSetupError, match="Invalid access token: 'live_123'"):
        client.set_access_token('live_123')

    with pytest.raises(RequestSetupError, match="Invalid access token: 'test_123'"):
        client.set_access_token('test_123')


def test_client_api_key_during_init_deprecated(recwarn):
    """Setting the api key during init should work but raise a warning."""
    with pytest.warns(PendingDeprecationWarning,
                      match='Setting the API key during init will be removed in the future'):
        client = Client(api_key='test_123')
    assert client.api_key == 'test_123'


def test_client_broken_cert_bundle(monkeypatch):
    """
    A request should raise an error when the certificate bundle is not available.

    Under circumstances it could be possible that the certifi package is not correctly installed, broken,
    or just plain too old. Connecting to the Mollie API should fail with an error when the certificate
    cannot be verified.

    We monkeypatch requests with a non-existent path at the location where certifi normally sets the correct path.
    """
    monkeypatch.setattr(requests.adapters, 'DEFAULT_CA_BUNDLE_PATH', '/does/not/exist')

    client = Client()
    client.set_api_key('test_test')
    with pytest.raises(
            RequestError,
            match='Could not find a suitable TLS CA certificate bundle, invalid path: /does/not/exist'):
        client.customers.list()


def test_client_generic_request_error(response):
    """
    When the remote server refuses connections or other request issues arise, an error should be raised.

    The 'response' fixture blocks all outgoing connections, also when no actual responses are configured.
    """
    client = Client()
    client.set_api_key('test_test')
    client.set_api_endpoint('https://api.mollie.invalid/')
    with pytest.raises(RequestError, match='Unable to communicate with Mollie: Connection refused'):
        client.customers.list()


def test_client_invalid_create_data(client):
    """Invalid data for a create command should raise an error."""
    data = datetime.now()
    with pytest.raises(RequestSetupError, match='Error encoding parameters into JSON'):
        client.customers.create(data=data)


def test_client_invalid_update_data(client):
    """Invalid data for a create command should raise an error."""
    data = datetime.now()
    with pytest.raises(RequestSetupError, match='Error encoding parameters into JSON'):
        client.customers.update('cst_12345', data=data)


@pytest.mark.parametrize('endpoint, errorstr', [
    ('customers', "Invalid customer ID: 'invalid'. A customer ID should start with 'cst_'."),
    ('payments', "Invalid payment ID: 'invalid'. A payment ID should start with 'tr_'."),
    ('refunds', "Invalid refund ID: 'invalid'. A refund ID should start with 're_'."),
    ('orders', "Invalid order ID: 'invalid'. An order ID should start with 'ord_'."),
])
def test_client_get_invalid_id(client, endpoint, errorstr):
    """An invalid formatted object ID should raise an error."""
    with pytest.raises(IdentifierError, match=errorstr):
        getattr(client, endpoint).get('invalid')


@pytest.mark.parametrize('endpoint, errorstr', [
    ('customer_mandates', "Invalid mandate ID: 'invalid'. A mandate ID should start with 'mdt_'."),
    ('customer_payments', "Invalid payment ID: 'invalid'. A payment ID should start with 'tr_'."),
    ('customer_subscriptions', "Invalid subscription ID: 'invalid'. A subscription ID should start with 'sub_'."),
])
def test_client_get_customer_related_invalid_id(client, endpoint, errorstr):
    """An invalid formatted object ID should raise an error."""
    with pytest.raises(IdentifierError, match=errorstr):
        getattr(client, endpoint).with_parent_id('cst_12345').get('invalid')


@pytest.mark.parametrize('endpoint, errorstr', [
    ('payment_chargebacks', "Invalid chargeback ID: 'invalid'. A chargeback ID should start with 'chb_'."),
    ('payment_refunds', "Invalid refund ID: 'invalid'. A refund ID should start with 're_'."),
])
def test_client_get_payment_related_invalid_id(client, endpoint, errorstr):
    """An invalid formatted object ID should raise an error."""
    with pytest.raises(IdentifierError, match=errorstr):
        getattr(client, endpoint).with_parent_id('tr_12345').get('invalid')


def test_client_invalid_json_response(client, response):
    """An invalid json response should raise an error."""
    response.get('https://api.mollie.com/v2/customers', 'invalid_json')
    with pytest.raises(ResponseHandlingError, match=r'Unable to decode Mollie API response \(status code: 200\)'):
        client.customers.list()


@pytest.mark.parametrize('resp_payload, resp_status, exception, errormsg', [
    ('error_unauthorized', 401, UnauthorizedError, 'Missing authentication, or failed to authenticate'),
    ('customer_doesnotexist', 404, NotFoundError, 'No customer exists with token cst_doesnotexist.'),
    ('payment_rejected', 422, UnprocessableEntityError, 'The amount is higher than the maximum'),
    ('error_teapot', 418, ResponseError, 'Just an example error that is not explicitly supported'),
])
def test_client_get_received_error_response(client, response, resp_payload, resp_status, exception, errormsg):
    """An error response from the API should raise a matching error."""
    response.get('https://api.mollie.com/v2/customers/cst_doesnotexist', resp_payload, status=resp_status)
    with pytest.raises(exception, match=errormsg) as excinfo:
        client.customers.get('cst_doesnotexist')
    assert excinfo.value.status == resp_status


@pytest.mark.parametrize('resp_payload, resp_status, exception, errormsg', [
    ('error_unauthorized', 401, UnauthorizedError, 'Missing authentication, or failed to authenticate'),
    ('customer_doesnotexist', 404, NotFoundError, 'No customer exists with token cst_doesnotexist.'),
    ('error_teapot', 418, ResponseError, 'Just an example error that is not explicitly supported'),
])
def test_client_delete_received_error_response(client, response, resp_payload, resp_status, exception, errormsg):
    """When deleting, an error response from the API should raise a matching error."""
    response.delete('https://api.mollie.com/v2/customers/cst_doesnotexist', resp_payload, status=resp_status)
    with pytest.raises(exception, match=errormsg) as excinfo:
        client.customers.delete('cst_doesnotexist')
    assert excinfo.value.status == resp_status


def test_client_response_404_but_no_payload(response):
    """
    An error response from the API should raise an error.

    When the response returns an error, but no valid error data is available in the response,
    we should still raise an error. The API v1 formatted error in the test is missing the required 'status' field.
    """
    response.get('https://api.mollie.com/v3/customers', 'v1_api_error', status=404)
    client = Client()
    client.api_version = 'v3'
    client.set_api_key('test_test')

    with pytest.raises(ResponseHandlingError, match='Invalid API version'):
        client.customers.list()


def test_client_error_including_field_response(client, response):
    """An error response containing a 'field' value should be reflected in the raised error."""
    response.post('https://api.mollie.com/v2/payments', 'payment_rejected', status=422)
    params = {
        'amount': {
            'value': '10000000.00',
            'currency': 'EUR',
        },
        'method': 'ideal',
        'description': 'My order',
        'redirectUrl': 'https://webshop.example.org/order/12345/',
        'webhookUrl': 'https://webshop.example.org/payments/webhook/',
    }
    with pytest.raises(UnprocessableEntityError, match='The amount is higher than the maximum') as excinfo:
        client.payments.create(**params)
    assert excinfo.value.field == 'amount'


@pytest.mark.skipif(sys.version_info.major != 2, reason='output differs for python 2')
def test_client_unicode_error_py2(client, response):
    """An error response containing Unicode characters should also be processed correctly."""
    response.post('https://api.mollie.com/v2/orders', 'order_error', status=422)
    with pytest.raises(UnprocessableEntityError) as err:
        # actual POST data for creating an order can be found in test_orders.py
        client.orders.create({})

    # handling the error should work even when utf-8 characters (€) are in the response.
    exception = err.value
    expected = 'Order line 1 is invalid. VAT amount is off. ' \
               'Expected VAT amount to be 3.47 (21.00% over 20.00), got 3.10'
    assert str(exception) == expected


@pytest.mark.skipif(sys.version_info.major == 2, reason='output differs for python 2')
def test_client_unicode_error_py3(client, response):
    """An error response containing Unicode characters should also be processed correctly."""
    response.post('https://api.mollie.com/v2/orders', 'order_error', status=422)
    with pytest.raises(UnprocessableEntityError) as err:
        # actual POST data for creating an order can be found in test_orders.py
        client.orders.create({})

    # handling the error should work even when utf-8 characters (€) are in the response.
    exception = err.value
    expected = 'Order line 1 is invalid. VAT amount is off. ' \
               'Expected VAT amount to be €3.47 (21.00% over €20.00), got €3.10'
    assert str(exception) == expected


@mock.patch('mollie.api.client.requests.request')
def test_client_request_timeout(request_mock, client):
    """Mock requests.request in the client to be able to read if the timeout is in the request call args."""
    response = mock.Mock(status_code=200)
    response.json.return_value = {}
    response.headers.get.return_value = 'application/hal+json'
    request_mock.return_value = response

    client.set_timeout(300)
    client.payments.list()
    assert request_mock.call_args[1]['timeout'] == 300


@mock.patch('mollie.api.client.requests.request')
def test_client_request_timed_out(request_mock, client):
    """Timeout should raise a RequestError."""
    request_mock.side_effect = requests.exceptions.ReadTimeout(
        "HTTPSConnectionPool(host='api.mollie.com', port=443): Read timed out. (read timeout=10)")

    with pytest.raises(RequestError, match='Read timed out.'):
        client.payments.list()


def test_client_data_consistency_error(client, response):
    """When the API sends us data we did not expect raise an consistency error."""
    order_id = 'ord_kEn1PlbGa'
    line_id = 'odl_12345'
    response.get('https://api.mollie.com/v2/orders/{order_id}'.format(order_id=order_id), 'order_single')
    response.patch('https://api.mollie.com/v2/orders/{order_id}/lines/{order_line_id}'.format(
        order_id=order_id, order_line_id=line_id), 'order_single')

    order = client.orders.get(order_id)
    data = {
        "name": "LEGO 71043 Hogwarts™ Castle",
    }
    # Update an nonexistent order line. This raises an data consistency error.
    with pytest.raises(DataConsistencyError, match=r'Line id .* not found in response.'):
        order.update_line(line_id, data)


def test_client_default_user_agent(client, response):
    """Default user-agent should contain some known values."""

    regex = re.compile(r'^Mollie/[\d\.]+ Python/[\d\.]+ OpenSSL/\w+')
    assert re.match(regex, client.user_agent)

    # perform a request and inpect the actual used headers
    response.get('https://api.mollie.com/v2/methods', 'methods_list')
    client.methods.list()
    request = response.calls[0].request
    assert re.match(regex, request.headers['User-Agent'])


def test_client_user_agent_with_oauth():
    """When authenticating with an access token, the User-Agent should cont an OAuth component."""
    client = Client()
    assert 'OAuth'.lower() not in client.user_agent.lower()
    client.set_access_token('access_123')
    assert 'OAuth/2.0' in client.user_agent


def test_client_set_user_agent_component(response):
    """We should be able to add useragent components.

    Note: we don't use the fixture client because it is shared between tests, and we don't want it
    to be clobbered with random User-Agent strings.
    """
    client = Client()
    assert 'Hoeba' not in client.user_agent
    client.set_user_agent_component('Hoeba', '1.0.0')
    assert 'Hoeba/1.0.0' in client.user_agent

    response.get('https://api.mollie.com/v2/methods', 'methods_list')
    client.set_api_key('test_123')
    client.methods.list()
    request = response.calls[0].request
    assert 'Hoeba/1.0.0' in request.headers['User-Agent']


@pytest.mark.parametrize("key, expected", [
    ('lowercase', 'Lowercase'),
    ('UPPERCASE', 'Uppercase'),
    ('multiple words', 'MultipleWords'),
    ('multiple   spaces', 'MultipleSpaces'),
    ('trailing space ', 'TrailingSpace')
])
def test_client_set_user_agent_component_correct_key_syntax(key, expected):
    """When we receive UA component keys that don't adhere to the proposed syntax, they are corrected."""
    client = Client()
    client.set_user_agent_component(key, '1.0.0')
    assert "{expected}/1.0.0".format(expected=expected) in client.user_agent


@pytest.mark.parametrize("value, expected", [
    ('1.2.3', '1.2.3'),
    ('singleword', 'singleword'),
    ('MiXedCaSe', 'MiXedCaSe'),  # should be preserved
    ('UPPERCASE', 'UPPERCASE'),  # should be preserved
    ('with space', 'with_space'),
    ('multiple   spaces', 'multiple_spaces'),
    ('trailing space ', 'trailing_space')
])
def test_client_set_user_agent_component_correct_value_syntax(value, expected):
    """When we receive UA component values that don't adhere to the proposed syntax, they are corrected."""
    client = Client()
    client.set_user_agent_component('Something', value)
    assert "Something/{expected}".format(expected=expected) in client.user_agent


def test_client_update_user_agent_component():
    """We should be able to update the User-Agent component when using the same key."""
    client = Client()
    client.set_user_agent_component('Test', '1.0.0')
    assert 'Test/1.0.0' in client.user_agent

    # now update the component using the same key
    client.set_user_agent_component('Test', '2.0.0')
    assert 'Test/2.0.0' in client.user_agent
    assert 'Test/1.0.0' not in client.user_agent

    # and update with a key that will be converted to the same value
    client.set_user_agent_component('TEST', '3.0.0')
    assert 'Test/3.0.0' in client.user_agent
    assert 'Test/2.0.0' not in client.user_agent
    assert 'Test/1.0.0' not in client.user_agent
