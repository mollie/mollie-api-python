import platform
import sys
import ssl
import re
import pkg_resources
try:
    from urllib.parse import urlencode
except ImportError:
    # support python 2
    from urllib import urlencode

import requests

from . import Error
from . import resources


class Client(object):
    CLIENT_VERSION = '2.0.0a0'
    API_ENDPOINT   = 'https://api.mollie.com'
    API_VERSION    = 'v2'
    UNAME          = ' '.join(platform.uname())
    USER_AGENT     = ' '.join(vs.replace(r'\s+', '-') for vs in [
        'Mollie/'  + CLIENT_VERSION,
        'Python/'  + sys.version.split(' ')[0],
        'OpenSSL/' + ssl.OPENSSL_VERSION.split(' ')[1],
    ])

    @staticmethod
    def validate_api_endpoint(api_endpoint):
        return api_endpoint.strip().rstrip('/')

    @staticmethod
    def validate_api_key(api_key):
        api_key = api_key.strip()
        if not re.compile(r'^(live|test)_\w+$').match(api_key):
            raise Error('Invalid API key: "%s". An API key must start with "test_" or "live_".' % api_key)
        return api_key

    def __init__(self, api_key=None, api_endpoint=None):
        self.api_endpoint = self.validate_api_endpoint(api_endpoint or self.API_ENDPOINT)
        self.api_version = self.API_VERSION
        self.api_key = self.validate_api_key(api_key) if api_key else None
        self.payments = resources.Payments(self)
        self.payment_refunds = resources.PaymentRefunds(self)
        self.payment_chargebacks = resources.PaymentChargebacks(self)
        self.methods = resources.Methods(self)
        self.issuers = resources.Issuers(self)
        self.refunds = resources.Refunds(self)
        self.chargebacks = resources.Chargebacks(self)
        self.customers = resources.Customers(self)
        self.customer_mandates = resources.CustomerMandates(self)
        self.customer_subscriptions = resources.CustomerSubscriptions(self)
        self.customer_payments = resources.CustomerPayments(self)

    def get_api_endpoint(self):
        return self.api_endpoint

    def set_api_endpoint(self, api_endpoint):
        self.api_endpoint = self.validate_api_endpoint(api_endpoint)

    def set_api_key(self, api_key):
        self.api_key = self.validate_api_key(api_key)

    def get_cacert(self):
        cacert = pkg_resources.resource_filename('mollie.api', 'cacert.pem')
        if not cacert or len(cacert) < 1:
            raise Error('Unable to load cacert.pem')
        return cacert

    def perform_http_call(self, http_method, path, data=None, params=None):
        if not self.api_key:
            raise Error('You have not set an API key. Please use setApiKey() to set the API key.')
        if path.startswith('%s/%s' % (self.api_endpoint, self.api_version)):
            url = path
        else:
            url = '%s/%s/%s' % (self.api_endpoint, self.api_version, path)
        data = '{}' if data is None else data

        querystring = generate_querystring(params)
        if querystring:
            url += '?' + querystring
            params = None

        try:
            response = requests.request(
                http_method, url,
                verify=self.get_cacert(),
                headers={
                    'Accept': 'application/json',
                    'Authorization': 'Bearer ' + self.api_key,
                    'User-Agent': self.USER_AGENT,
                    'X-Mollie-Client-Info': self.UNAME,
                },
                params=params,
                data=data
            )
        except Exception as e:
            raise Error('Unable to communicate with Mollie: %s.' % str(e))
        return response


def generate_querystring(params):
    """
    Generate a querystring suitable for use in the v2 api.

    The Requests library doesn't know how to generate querystrings that encode dictionaries using square brackets:
    https://api.mollie.com/v2/methods?amount[value]=100.00&amount[currency]=USD

    Note: we use `sorted()` to work around a difference in iteration behaviour between Python 2 and 3.
    This makes the output predictable, and ordering of querystring parameters shouldn't matter.
    """
    if not params:
        return
    parts = []
    for param, value in sorted(params.items()):
        if not isinstance(value, dict):
            parts.append(urlencode({param: value}))
        else:
            # encode dictionary with square brackets
            for key, sub_value in sorted(value.items()):
                composed = '%s[%s]' % (param, key)
                parts.append(urlencode({composed: sub_value}))
    if parts:
        return '&'.join(parts)
