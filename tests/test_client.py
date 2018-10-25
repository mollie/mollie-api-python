# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
from datetime import datetime

import mock
import pkg_resources
import pytest
import requests

from mollie.api.client import Client, generate_querystring
from mollie.api.error import (
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


def test_client_no_api_key():
    """A Request without an API key should raise an error."""
    client = Client()
    with pytest.raises(RequestSetupError) as excinfo:
        client.customers.list()
    assert excinfo.match('You have not set an API key.')


def test_client_invalid_api_key():
    """Setting up an invalid api key raises an error."""
    client = Client()
    with pytest.raises(RequestSetupError) as excinfo:
        client.set_api_key('invalid')
    assert excinfo.match("Invalid API key: 'invalid'")


def test_client_no_cert_bundle(monkeypatch):
    """A request should raise an error when the certificate bundle is not available."""

    def mockreturn(modulepath, file):
        return ''

    monkeypatch.setattr(pkg_resources, 'resource_filename', mockreturn)

    client = Client()
    client.set_api_key('test_test')
    with pytest.raises(RequestSetupError) as excinfo:
        client.customers.list()
    assert excinfo.match('Unable to load cacert.pem')


def test_client_generic_request_error(response):
    """
    When the remote server refuses connections or other request issues arise, an error should be raised.

    The 'response' fixture blocks all outgoing connections, also when no actual responses are configured.
    """
    client = Client()
    client.set_api_key('test_test')
    client.set_api_endpoint('https://api.mollie.invalid/')
    with pytest.raises(RequestError) as excinfo:
        client.customers.list()
    assert excinfo.match('Unable to communicate with Mollie: Connection refused')


def test_client_invalid_create_data(client):
    """Invalid data for a create command should raise an error."""
    data = datetime.now()
    with pytest.raises(RequestSetupError) as excinfo:
        client.customers.create(data=data)
    assert excinfo.match('Error encoding parameters into JSON')


def test_client_invalid_update_data(client):
    """Invalid data for a create command should raise an error."""
    data = datetime.now()
    with pytest.raises(RequestSetupError) as excinfo:
        client.customers.update('cst_12345', data=data)
    assert excinfo.match('Error encoding parameters into JSON')


@pytest.mark.parametrize('endpoint, errorstr', [
    ('customers', "Invalid customer ID: 'invalid'. A customer ID should start with 'cst_'."),
    ('payments', "Invalid payment ID: 'invalid'. A payment ID should start with 'tr_'."),
    ('refunds', "Invalid refund ID: 'invalid'. A refund ID should start with 're_'."),
    ('orders', "Invalid order ID: 'invalid'. An order ID should start with 'ord_'."),
])
def test_client_get_invalid_id(client, endpoint, errorstr):
    """An invalid formatted object ID should raise an error."""
    with pytest.raises(IdentifierError) as excinfo:
        getattr(client, endpoint).get('invalid')
    assert excinfo.match(errorstr)


@pytest.mark.parametrize('endpoint, errorstr', [
    ('customer_mandates', "Invalid mandate ID: 'invalid'. A mandate ID should start with 'mdt_'."),
    ('customer_payments', "Invalid payment ID: 'invalid'. A payment ID should start with 'tr_'."),
    ('customer_subscriptions', "Invalid subscription ID: 'invalid'. A subscription ID should start with 'sub_'."),
])
def test_client_get_customer_related_invalid_id(client, endpoint, errorstr):
    """An invalid formatted object ID should raise an error."""
    with pytest.raises(IdentifierError) as excinfo:
        getattr(client, endpoint).with_parent_id('cst_12345').get('invalid')
    assert excinfo.match(errorstr)


@pytest.mark.parametrize('endpoint, errorstr', [
    ('payment_chargebacks', "Invalid chargeback ID: 'invalid'. A chargeback ID should start with 'chb_'."),
    ('payment_refunds', "Invalid refund ID: 'invalid'. A refund ID should start with 're_'."),
])
def test_client_get_payment_related_invalid_id(client, endpoint, errorstr):
    """An invalid formatted object ID should raise an error."""
    with pytest.raises(IdentifierError) as excinfo:
        getattr(client, endpoint).with_parent_id('tr_12345').get('invalid')
    assert excinfo.match(errorstr)


def test_client_invalid_json_response(client, response):
    """An invalid json response should raise an error."""
    response.get('https://api.mollie.com/v2/customers', 'invalid_json')
    with pytest.raises(ResponseHandlingError) as excinfo:
        client.customers.list()
    assert excinfo.match(r'Unable to decode Mollie API response \(status code: 200\)')


@pytest.mark.parametrize('resp_payload, resp_status, exception, errormsg', [
    ('error_unauthorized', 401, UnauthorizedError, 'Missing authentication, or failed to authenticate'),
    ('customer_doesnotexist', 404, NotFoundError, 'No customer exists with token cst_doesnotexist.'),
    ('payment_rejected', 422, UnprocessableEntityError, 'The amount is higher than the maximum'),
    ('error_teapot', 418, ResponseError, 'Just an example error that is not explicitly supported'),
])
def test_client_get_received_error_response(client, response, resp_payload, resp_status, exception, errormsg):
    """An error response from the API should raise a matching error."""
    response.get('https://api.mollie.com/v2/customers/cst_doesnotexist', resp_payload, status=resp_status)
    with pytest.raises(exception) as excinfo:
        client.customers.get('cst_doesnotexist')
    assert excinfo.match(errormsg)
    assert excinfo.value.status == resp_status


@pytest.mark.parametrize('resp_payload, resp_status, exception, errormsg', [
    ('error_unauthorized', 401, UnauthorizedError, 'Missing authentication, or failed to authenticate'),
    ('customer_doesnotexist', 404, NotFoundError, 'No customer exists with token cst_doesnotexist.'),
    ('error_teapot', 418, ResponseError, 'Just an example error that is not explicitly supported'),
])
def test_client_delete_received_error_response(client, response, resp_payload, resp_status, exception, errormsg):
    """When deleting, an error response from the API should raise a matching error."""
    response.delete('https://api.mollie.com/v2/customers/cst_doesnotexist', resp_payload, status=resp_status)
    with pytest.raises(exception) as excinfo:
        client.customers.delete('cst_doesnotexist')
    assert excinfo.match(errormsg)
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

    with pytest.raises(ResponseHandlingError) as excinfo:
        client.customers.list()
    assert excinfo.match('Invalid API version')


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
    with pytest.raises(UnprocessableEntityError) as excinfo:
        client.payments.create(**params)
    assert excinfo.match('The amount is higher than the maximum')
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

    with pytest.raises(RequestError) as err:
        client.payments.list()
    assert "Read timed out." in str(err.value)
