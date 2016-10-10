import platform
import sys
import ssl
import re
import pkg_resources

import requests

from .Error import *


class Client:
    CLIENT_VERSION = '1.1.3'
    HTTP_GET = 'GET'
    HTTP_POST = 'POST'
    HTTP_DELETE = 'DELETE'
    API_ENDPOINT = 'https://api.mollie.nl'
    API_VERSION = 'v1'

    def __init__(self):
        from . import Resource

        self.api_endpoint = self.API_ENDPOINT
        self.api_version = self.API_VERSION
        self.api_key = ''
        self.payments = Resource.Payments(self)
        self.payment_refunds = Resource.Refunds(self)
        self.issuers = Resource.Issuers(self)
        self.methods = Resource.Methods(self)
        self.version_strings = []
        self.addVersionString('Mollie/' + self.CLIENT_VERSION)
        self.addVersionString('Python/' + sys.version.split(' ')[0])
        self.addVersionString('OpenSSL/' + ssl.OPENSSL_VERSION.split(' ')[1])

    def getApiEndpoint(self):
        return self.api_endpoint

    def setApiEndpoint(self, api_endpoint):
        self.api_endpoint = api_endpoint.strip().rstrip('/')

    def setApiKey(self, api_key):
        api_key = api_key.strip()
        if not re.compile('^(live|test)_\w+$').match(api_key):
            raise Error('Invalid API key: "%s". An API key must start with "test_" or "live_".' % api_key)
        self.api_key = api_key

    def addVersionString(self, version_string):
        self.version_strings.append(version_string.replace(r'\s+', '-'))

    def getCACert(self):
        cacert = pkg_resources.resource_filename('Mollie.API', 'cacert.pem')
        if not cacert or len(cacert) < 1:
            raise Error('Unable to load cacert.pem')
        return cacert

    def performHttpCall(self, http_method, path, data=None, params=None):
        if not self.api_key:
            raise Error('You have not set an API key. Please use setApiKey() to set the API key.')
        url = self.api_endpoint + '/' + self.api_version + '/' + path
        user_agent = ' '.join(self.version_strings)
        uname = ' '.join(platform.uname())
        try:
            response = requests.request(
                http_method, url,
                verify=self.getCACert(),
                headers={
                    'Accept': 'application/json',
                    'Authorization': 'Bearer ' + self.api_key,
                    'User-Agent': user_agent,
                    'X-Mollie-Client-Info': uname
                },
                params=params,
                data=data
            )
        except Exception as e:
            raise Error('Unable to communicate with Mollie: %s.' % e.message)
        return response
