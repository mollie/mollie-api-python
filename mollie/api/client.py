import platform
import re
import ssl
import sys

import pkg_resources
import requests

from .error import RequestError, RequestSetupError
from .resources.chargebacks import Chargebacks
from .resources.customer_mandates import CustomerMandates
from .resources.customer_payments import CustomerPayments
from .resources.customer_subscriptions import CustomerSubscriptions
from .resources.customers import Customers
from .resources.methods import Methods
from .resources.payment_chargebacks import PaymentChargebacks
from .resources.payment_refunds import PaymentRefunds
from .resources.payments import Payments
from .resources.refunds import Refunds

try:
    from urllib.parse import urlencode
except ImportError:
    # support python 2
    from urllib import urlencode


class Client(object):
    CLIENT_VERSION = '2.0.0a0'
    API_ENDPOINT = 'https://api.mollie.com'
    API_VERSION = 'v2'
    UNAME = ' '.join(platform.uname())
    USER_AGENT = ' '.join(vs.replace(r'\s+', '-') for vs in [
        'Mollie/' + CLIENT_VERSION,
        'Python/' + sys.version.split(' ')[0],
        'OpenSSL/' + ssl.OPENSSL_VERSION.split(' ')[1],
    ])

    @staticmethod
    def validate_api_endpoint(api_endpoint):
        return api_endpoint.strip().rstrip('/')

    @staticmethod
    def validate_api_key(api_key):
        api_key = api_key.strip()
        if not re.compile(r'^(live|test)_\w+$').match(api_key):
            raise RequestSetupError('Invalid API key: "%s". An API key must start with "test_" or "live_".' % api_key)
        return api_key

    def __init__(self, api_key=None, api_endpoint=None):
        self.api_endpoint = self.validate_api_endpoint(api_endpoint or self.API_ENDPOINT)
        self.api_version = self.API_VERSION
        self.api_key = self.validate_api_key(api_key) if api_key else None
        self.payments = Payments(self)
        self.payment_refunds = PaymentRefunds(self)
        self.payment_chargebacks = PaymentChargebacks(self)
        self.methods = Methods(self)
        self.refunds = Refunds(self)
        self.chargebacks = Chargebacks(self)
        self.customers = Customers(self)
        self.customer_mandates = CustomerMandates(self)
        self.customer_subscriptions = CustomerSubscriptions(self)
        self.customer_payments = CustomerPayments(self)

    def get_api_endpoint(self):
        return self.api_endpoint

    def set_api_endpoint(self, api_endpoint):
        self.api_endpoint = self.validate_api_endpoint(api_endpoint)

    def set_api_key(self, api_key):
        self.api_key = self.validate_api_key(api_key)

    def get_cacert(self):
        cacert = pkg_resources.resource_filename('mollie.api', 'cacert.pem')
        if not cacert or len(cacert) < 1:
            raise RequestSetupError('Unable to load cacert.pem')
        return cacert

    def perform_http_call(self, http_method, path, data=None, params=None):
        if not self.api_key:
            raise RequestSetupError('You have not set an API key. Please use set_api_key() to set the API key.')
        if path.startswith('%s/%s' % (self.api_endpoint, self.api_version)):
            url = path
        else:
            url = '%s/%s/%s' % (self.api_endpoint, self.api_version, path)
        data = '{}' if data is None else data

        querystring = generate_querystring(params)
        if querystring:
            url += '?' + querystring
            params = None

        cacert = self.get_cacert()
        try:
            response = requests.request(
                http_method, url,
                verify=cacert,
                headers={
                    'Accept': 'application/json',
                    'Authorization': 'Bearer ' + self.api_key,
                    'User-Agent': self.USER_AGENT,
                    'X-Mollie-Client-Info': self.UNAME,
                },
                params=params,
                data=data
            )
        except Exception as err:
            raise RequestError('Unable to communicate with Mollie: %s' % err)
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
