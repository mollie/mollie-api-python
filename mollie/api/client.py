from __future__ import annotations

import json
import platform
import re
import ssl
from collections import OrderedDict
from typing import TYPE_CHECKING, Any, Callable, Optional, Union
from urllib.parse import urlencode

import requests
import requests_oauthlib
from urllib3.util import Retry

from .error import RequestError, RequestSetupError
from .resources.captures import Captures
from .resources.chargebacks import Chargebacks
from .resources.customer_mandates import CustomerMandates
from .resources.customer_payments import CustomerPayments
from .resources.customer_subscriptions import CustomerSubscriptions
from .resources.customers import Customers
from .resources.invoices import Invoices
from .resources.methods import Methods
from .resources.onboarding import Onboarding
from .resources.orders import Orders
from .resources.organizations import Organizations
from .resources.payment_chargebacks import PaymentChargebacks
from .resources.payment_links import PaymentLinks
from .resources.payment_refunds import PaymentRefunds
from .resources.payments import Payments
from .resources.permissions import Permissions
from .resources.profile_chargebacks import ProfileChargebacks
from .resources.profile_methods import ProfileMethods
from .resources.profile_payments import ProfilePayments
from .resources.profile_refunds import ProfileRefunds
from .resources.profiles import Profiles
from .resources.refunds import Refunds
from .resources.settlement_captures import SettlementCaptures
from .resources.settlement_chargebacks import SettlementChargebacks
from .resources.settlement_payments import SettlementPayments
from .resources.settlement_refunds import SettlementRefunds
from .resources.settlements import Settlements
from .resources.subscription_payments import SubscriptionPayments
from .resources.subscriptions import Subscriptions
from .version import VERSION

if TYPE_CHECKING:
    from .typing import Timeout


class Client(object):
    CLIENT_VERSION: str = VERSION
    API_ENDPOINT: str = "https://api.mollie.com"
    API_VERSION: str = "v2"
    UNAME: str = " ".join(platform.uname())

    OAUTH_AUTHORIZATION_URL: str = "https://www.mollie.com/oauth2/authorize"
    OAUTH_AUTO_REFRESH_URL: str = API_ENDPOINT + "/oauth2/tokens"
    OAUTH_TOKEN_URL: str = API_ENDPOINT + "/oauth2/tokens"

    access_token: Union[dict[Any, Any], None]
    api_key: Union[str, None]
    client_secret = Union[str, None]
    set_token: Union[Callable, None]
    user_agent_components: dict[str, str]
    _client: Union[requests.Session, None]
    _oauth_client: Union[requests_oauthlib.OAuth2Session, None]

    @staticmethod
    def validate_api_endpoint(api_endpoint: str) -> str:
        return api_endpoint.strip().rstrip("/")

    @staticmethod
    def validate_api_key(api_key: str) -> str:
        api_key = api_key.strip()
        if not re.compile(r"^(live|test)_\w+$").match(api_key):
            raise RequestSetupError(f"Invalid API key: '{api_key}'. An API key must start with 'test_' or 'live_'.")
        return api_key

    @staticmethod
    def validate_access_token(access_token: str) -> str:
        access_token = access_token.strip()
        if not access_token.startswith("access_"):
            raise RequestSetupError(
                f"Invalid access token: '{access_token}'. An access token must start with 'access_'."
            )
        return access_token

    def __init__(self, api_endpoint: str = None, timeout: Timeout = (2, 10), retry: int = 3):
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
        self.payment_refunds = PaymentRefunds(self)
        self.payment_chargebacks = PaymentChargebacks(self)
        self.profiles = Profiles(self)
        self.profile_chargebacks = ProfileChargebacks(self)
        self.profile_methods = ProfileMethods(self)
        self.profile_payments = ProfilePayments(self)
        self.profile_refunds = ProfileRefunds(self)
        self.methods = Methods(self)
        self.refunds = Refunds(self)
        self.chargebacks = Chargebacks(self)
        self.customers = Customers(self)
        self.customer_mandates = CustomerMandates(self)
        self.customer_subscriptions = CustomerSubscriptions(self)
        self.customer_payments = CustomerPayments(self)
        self.orders = Orders(self)
        self.organizations = Organizations(self)
        self.subscription_payments = SubscriptionPayments(self)
        self.invoices = Invoices(self)
        self.permissions = Permissions(self)
        self.onboarding = Onboarding(self)
        self.captures = Captures(self)
        self.settlements = Settlements(self)
        self.settlement_payments = SettlementPayments(self)
        self.settlement_refunds = SettlementRefunds(self)
        self.settlement_chargebacks = SettlementChargebacks(self)
        self.settlement_captures = SettlementCaptures(self)
        self.subscriptions = Subscriptions(self)

        # compose base user agent string
        self.user_agent_components = OrderedDict()
        self.set_user_agent_component("Mollie", self.CLIENT_VERSION)
        self.set_user_agent_component("Python", platform.python_version())
        self.set_user_agent_component(
            "OpenSSL", ssl.OPENSSL_VERSION.split(" ")[1], sanitize=False
        )  # keep legacy formatting of this component

    def set_api_endpoint(self, api_endpoint: str) -> None:
        self.api_endpoint = self.validate_api_endpoint(api_endpoint)

    def set_api_key(self, api_key: str) -> None:
        self.api_key = self.validate_api_key(api_key)

    def set_access_token(self, access_token: str) -> None:
        self.api_key = self.validate_access_token(access_token)
        self.set_user_agent_component("OAuth", "2.0", sanitize=False)  # keep spelling equal to the PHP client

    def set_timeout(self, timeout: Timeout) -> None:
        self.timeout = timeout

    def set_user_agent_component(self, key: str, value: str, sanitize: bool = True) -> None:
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
    def user_agent(self) -> str:
        """Return the formatted user agent string."""
        components = ["/".join(x) for x in self.user_agent_components.items()]
        return " ".join(components)

    def _format_request_data(self, path: str, data, params):
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

    def _perform_http_call_apikey(
        self,
        http_method: str,
        path: str,
        data: Optional[dict[Any, Any]] = None,
        params: Optional[dict[Any, Any]] = None,
    ) -> requests.Response:
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

    def _perform_http_call_oauth(
        self,
        http_method: str,
        path: str,
        data: Optional[dict[Any, Any]] = None,
        params: Optional[dict[Any, Any]] = None,
    ) -> requests.Response:
        if not self._oauth_client:
            raise RequestSetupError(
                "You have not setup the oauth client. Please use setup_oauth() before performing an oauth request."
            )

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

    def perform_http_call(
        self,
        http_method: str,
        path: str,
        data: Optional[dict[Any, Any]] = None,
        params: Optional[dict[Any, Any]] = None,
    ) -> requests.Response:
        if self._oauth_client:
            return self._perform_http_call_oauth(http_method, path, data=data, params=params)
        else:
            return self._perform_http_call_apikey(http_method, path, data=data, params=params)

    def setup_oauth(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scope: tuple[str, ...],
        token: dict[Any, Any],
        set_token: Callable,
    ) -> tuple[Any, Optional[Any]]:
        """
        :param client_id: (string)
        :param client_secret: (string)
        :param redirect_uri: (string)
        :param scope: Mollie connect permissions (tuple)
        :param token: The stored token (dict)
        :param set_token: Callable that stores a token (dict)
        :return: authorization url (url)
        """
        self.set_user_agent_component("OAuth", "2.0", sanitize=False)  # keep spelling equal to the PHP client
        self.set_token = set_token
        self.client_secret = client_secret
        self._oauth_client = requests_oauthlib.OAuth2Session(
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

    def setup_oauth_authorization_response(self, authorization_response) -> dict[Any, Any]:
        """
        :param authorization_response: The full callback URL (string)
        :return: None
        """
        if not self._oauth_client or not self.set_token:
            raise RequestSetupError(
                "You have not setup the oauth client. Please use setup_oauth() before performing an oauth request."
            )

        # Fetch an access token from the provider using the authorization code obtained during user authorization.
        access_token = self._oauth_client.fetch_token(
            self.OAUTH_TOKEN_URL,
            authorization_response=authorization_response,
            client_secret=self.client_secret,
        )

        self.set_token(access_token)
        self.access_token = access_token
        return access_token

    def _setup_retry(self) -> None:
        """Configure a retry behaviour on the HTTP client."""
        if self.retry:
            retry = Retry(connect=self.retry, backoff_factor=1)
            adapter = requests.adapters.HTTPAdapter(max_retries=retry)

            if self._client:
                self._client.mount("https://", adapter)
            if self._oauth_client:
                self._oauth_client.mount("https://", adapter)


def generate_querystring(params: dict[Any, Any]) -> Union[None, str]:
    """
    Generate a querystring suitable for use in the v2 api.

    The Requests library doesn't know how to generate querystrings that encode dictionaries using square brackets:
    https://api.mollie.com/v2/methods?amount[value]=100.00&amount[currency]=USD

    Note: we use `sorted()` to work around a difference in iteration behaviour between Python 2 and 3.
    This makes the output predictable, and ordering of querystring parameters shouldn't matter.
    """
    if not params:
        return None
    parts = []
    for param, value in sorted(params.items()):
        if not isinstance(value, dict):
            parts.append(urlencode({param: value}))
        else:
            # encode dictionary with square brackets
            for key, sub_value in sorted(value.items()):
                composed = f"{param}[{key}]"
                parts.append(urlencode({composed: sub_value}))
    if parts:
        return "&".join(parts)
    else:
        return None
