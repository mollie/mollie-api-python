import platform
import sys
import ssl
import re
import pkg_resources

import requests

from . import Error
from . import Resource


class Client(object):
    CLIENT_VERSION = '1.2.1'
    API_ENDPOINT   = 'https://api.mollie.nl'
    API_VERSION    = 'v1'
    UNAME          = ' '.join(platform.uname())
    USER_AGENT     = ' '.join(vs.replace(r'\s+', '-') for vs in [
        'Mollie/'  + CLIENT_VERSION,
        'Python/'  + sys.version.split(' ')[0],
        'OpenSSL/' + ssl.OPENSSL_VERSION.split(' ')[1],
    ])

    @staticmethod
    def validateApiEndpoint(api_endpoint):
        return api_endpoint.strip().rstrip('/')

    @staticmethod
    def validateApiKey(api_key):
        api_key = api_key.strip()
        if not re.compile(r'^(live|test)_\w+$').match(api_key):
            raise Error('Invalid API key: "%s". An API key must start with "test_" or "live_".' % api_key)
        return api_key

    def __init__(self, api_key=None, api_endpoint=None):
        self.api_endpoint = self.validateApiEndpoint(api_endpoint or self.API_ENDPOINT)
        self.api_version = self.API_VERSION
        self.api_key = self.validateApiKey(api_key) if api_key else None
        self.payments = Resource.Payments(self)
        self.payment_refunds = Resource.PaymentRefunds(self)
        self.payment_chargebacks = Resource.PaymentChargebacks(self)
        self.methods = Resource.Methods(self)
        self.issuers = Resource.Issuers(self)
        self.refunds = Resource.Refunds(self)
        self.chargebacks = Resource.Chargebacks(self)
        self.customers = Resource.Customers(self)
        self.customer_mandates = Resource.CustomerMandates(self)
        self.customer_subscriptions = Resource.CustomerSubscriptions(self)
        self.customer_payments = Resource.CustomerPayments(self)

    def getApiEndpoint(self):
        return self.api_endpoint

    def setApiEndpoint(self, api_endpoint):
        self.api_endpoint = self.validateApiEndpoint(api_endpoint)

    def setApiKey(self, api_key):
        self.api_key = self.validateApiKey(api_key)

    def getCACert(self):
        cacert = pkg_resources.resource_filename('Mollie.API', 'cacert.pem')
        if not cacert or len(cacert) < 1:
            raise Error('Unable to load cacert.pem')
        return cacert

    def performHttpCall(self, http_method, path, data=None, params=None):
        if not self.api_key:
            raise Error('You have not set an API key. Please use setApiKey() to set the API key.')
        url = '%s/%s/%s' % (self.api_endpoint, self.api_version, path)
        data = '{}' if data is None else data

        try:
            response = requests.request(
                http_method, url,
                verify=self.getCACert(),
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
