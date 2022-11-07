import json
import platform
import re
import ssl
from collections import OrderedDict
from urllib.parse import urlencode

import requests
from requests_oauthlib import OAuth2Session
from urllib3.util import Retry

from .error import RequestError, RequestSetupError
from .resources import (
    Chargebacks,
    Clients,
    Customers,
    Invoices,
    Methods,
    Onboarding,
    Orders,
    Organizations,
    PaymentLinks,
    Payments,
    Permissions,
    Profiles,
    Refunds,
    Settlements,
    Subscriptions,
)
from .version import VERSION


class Client(object):
    CLIENT_VERSION = VERSION
    API_ENDPOINT = "https://api.mollie.com"
    API_VERSION = "v2"
    UNAME = " ".join(platform.uname())

    OAUTH_AUTHORIZATION_URL = "https://www.mollie.com/oauth2/authorize"
    OAUTH_AUTO_REFRESH_URL = API_ENDPOINT + "/oauth2/tokens"
    OAUTH_TOKEN_URL = API_ENDPOINT + "/oauth2/tokens"

    @staticmethod
    def validate_api_endpoint(api_endpoint):
        return api_endpoint.strip().rstrip("/")

    @staticmethod
    def validate_api_key(api_key):
        api_key = api_key.strip()
        if not re.compile(r"^(live|test)_\w+$").match(api_key):
            raise RequestSetupError(f"Invalid API key: '{api_key}'. An API key must start with 'test_' or 'live_'.")
        return api_key

    @staticmethod
    def validate_access_token(access_token):
        access_token = access_token.strip()
        if not access_token.startswith("access_"):
            raise RequestSetupError(
                f"Invalid access token: '{access_token}'. An access token must start with 'access_'."
            )
        return access_token

    def __init__(self, api_endpoint=None, timeout=(2, 10), retry=3):
        """Initialize a new Mollie API client.

        :param api_endpoint: The API endpoint to communicate to, this default to the production environment (string)
        :param timeout: The timeouts used for the HTTP requests to the API, the default specifies both connect and
            read timeout (integer or tuple)
        :param retry: The number of retries that the client should perform in case of failed requests. Note that only
            connect errors trigger a retry, errors reponses from the API don't (integer).
        """
        self.api_endpoint = self.validate_api_endpoint(api_endpoint or self.API_ENDPOINT)
        self.api_version = self.API_VERSION
        self.timeout = timeout
        self.retry = retry
        self.api_key = None
        self._client = None

        self._oauth_client = None
        self.client_secret = None
        self.access_token = None
        self.set_token = None

        # add endpoint resources
        self.payments = Payments(self)
        self.payment_links = PaymentLinks(self)
        self.profiles = Profiles(self)
        self.methods = Methods(self)
        self.refunds = Refunds(self)
        self.chargebacks = Chargebacks(self)
        self.clients = Clients(self)
        self.customers = Customers(self)
        self.orders = Orders(self)
        self.organizations = Organizations(self)
        self.invoices = Invoices(self)
        self.permissions = Permissions(self)
        self.onboarding = Onboarding(self)
        self.settlements = Settlements(self)
        self.subscriptions = Subscriptions(self)

        # compose base user agent string
        self.user_agent_components = OrderedDict()
        self.set_user_agent_component("Mollie", self.CLIENT_VERSION)
        self.set_user_agent_component("Python", platform.python_version())
        self.set_user_agent_component(
            "OpenSSL", ssl.OPENSSL_VERSION.split(" ")[1], sanitize=False
        )  # keep legacy formatting of this component

    def set_api_endpoint(self, api_endpoint):
        self.api_endpoint = self.validate_api_endpoint(api_endpoint)

    def set_api_key(self, api_key):
        self.api_key = self.validate_api_key(api_key)

    def set_access_token(self, access_token):
        self.api_key = self.validate_access_token(access_token)
        self.set_user_agent_component("OAuth", "2.0", sanitize=False)  # keep spelling equal to the PHP client

    def set_timeout(self, timeout):
        self.timeout = timeout

    def set_user_agent_component(self, key, value, sanitize=True):
        """Add or replace new user-agent component strings.

        Given strings are formatted along the format agreed upon by Mollie and implementers:
        - key and values are separated by a forward slash ("/").
        - multiple key/values are separated by a space.
        - keys are camel-cased, and cannot contain spaces.
        - values cannot contain spaces.

        Note: When you set sanitize=false you need to make sure the formatting is correct yourself.
        """
        if sanitize:
            key = "".join(_x.capitalize() for _x in re.findall(r"\S+", key))
            if re.search(r"\s+", value):
                value = "_".join(re.findall(r"\S+", value))
        self.user_agent_components[key] = value

    @property
    def user_agent(self):
        """Return the formatted user agent string."""
        components = ["/".join(x) for x in self.user_agent_components.items()]
        return " ".join(components)

    def _format_request_data(self, path, data, params):
        if path.startswith(f"{self.api_endpoint}/{self.api_version}"):
            url = path
        else:
            url = f"{self.api_endpoint}/{self.api_version}/{path}"

        if data is not None:
            try:
                data = json.dumps(data)
            except Exception as err:
                raise RequestSetupError(f"Error encoding parameters into JSON: '{err}'.")

        querystring = generate_querystring(params)
        if querystring:
            url += "?" + querystring
            params = None

        return url, data, params

    def _perform_http_call_apikey(self, http_method, path, data=None, params=None):
        if not self.api_key:
            raise RequestSetupError("You have not set an API key. Please use set_api_key() to set the API key.")

        if not self._client:
            self._client = requests.Session()
            self._client.verify = True
            self._setup_retry()

        url, data, params = self._format_request_data(path, data, params)
        try:
            response = self._client.request(
                method=http_method,
                url=url,
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": self.user_agent,
                    "X-Mollie-Client-Info": self.UNAME,
                },
                params=params,
                data=data,
                timeout=self.timeout,
            )
        except requests.exceptions.RequestException as err:
            raise RequestError(f"Unable to communicate with Mollie: {err}")
        return response

    def _perform_http_call_oauth(self, http_method, path, data=None, params=None):
        url, data, params = self._format_request_data(path, data, params)
        try:
            response = self._oauth_client.request(
                method=http_method,
                url=url,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "User-Agent": self.user_agent,
                    "X-Mollie-Client-Info": self.UNAME,
                },
                params=params,
                data=data,
                timeout=self.timeout,
            )
        except requests.exceptions.RequestException as err:
            raise RequestError(f"Unable to communicate with Mollie: {err}")
        return response

    def perform_http_call(self, http_method, path, data=None, params=None):
        if self._oauth_client:
            return self._perform_http_call_oauth(http_method, path, data=data, params=params)
        else:
            return self._perform_http_call_apikey(http_method, path, data=data, params=params)

    def setup_oauth(self, client_id, client_secret, redirect_uri, scope, token, set_token):
        """
        :param client_id: (string)
        :param client_secret: (string)
        :param redirect_uri: (string)
        :param scope: Mollie connect permissions (list)
        :param token: The stored token (dict)
        :param set_token: Callable that stores a token (dict)
        :return: authorization url (url)
        """
        self.set_user_agent_component("OAuth", "2.0", sanitize=False)  # keep spelling equal to the PHP client
        self.set_token = set_token
        self.client_secret = client_secret
        self._oauth_client = OAuth2Session(
            client_id,
            auto_refresh_kwargs={
                "client_id": client_id,
                "client_secret": self.client_secret,
            },
            auto_refresh_url=self.OAUTH_AUTO_REFRESH_URL,
            redirect_uri=redirect_uri,
            scope=scope,
            token=token,
            token_updater=set_token,
        )
        self._oauth_client.verify = True
        self._setup_retry()

        authorization_url = None
        if not self._oauth_client.authorized:
            authorization_url, state = self._oauth_client.authorization_url(self.OAUTH_AUTHORIZATION_URL)

        # The merchant should visit this url to authorize access.
        return self._oauth_client.authorized, authorization_url

    def setup_oauth_authorization_response(self, authorization_response):
        """
        :param authorization_response: The full callback URL (string)
        :return: None
        """
        # Fetch an access token from the provider using the authorization code obtained during user authorization.
        self.access_token = self._oauth_client.fetch_token(
            self.OAUTH_TOKEN_URL,
            authorization_response=authorization_response,
            client_secret=self.client_secret,
        )
        self.set_token(self.access_token)
        return self.access_token

    # TODO Implement https://docs.mollie.com/reference/oauth2/revoke-token
    # def revoke_oauth_token(self, token, type_hint):
    #     ...

    def _setup_retry(self):
        """Configure a retry behaviour on the HTTP client."""
        if self.retry:
            retry = Retry(connect=self.retry, backoff_factor=1)
            adapter = requests.adapters.HTTPAdapter(max_retries=retry)

            if self._client:
                self._client.mount("https://", adapter)
            if self._oauth_client:
                self._oauth_client.mount("https://", adapter)


def generate_querystring(params):
    """
    Generate a querystring suitable for use in the v2 api.

    The Requests library doesn't know how to generate querystrings that encode dictionaries using square brackets:
    https://api.mollie.com/v2/methods?amount[value]=100.00&amount[currency]=USD
    """
    if not params:
        return None
    parts = []
    for param, value in params.items():
        if not isinstance(value, dict):
            parts.append(urlencode({param: value}))
        else:
            # encode dictionary with square brackets
            for key, sub_value in value.items():
                composed = f"{param}[{key}]"
                parts.append(urlencode({composed: sub_value}))
    if parts:
        return "&".join(parts)
