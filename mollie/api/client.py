import json
import platform
import re
import ssl
from collections import OrderedDict
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from urllib.parse import urlencode

import requests
from requests_oauthlib import OAuth2Session
from urllib3.util import Retry

from .error import RequestError, RequestSetupError
from .resources import (
    Balances,
    Chargebacks,
    ClientLinks,
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
    Terminals,
)
from .version import VERSION


class Client(object):
    CLIENT_VERSION: str = VERSION
    API_ENDPOINT: str = "https://api.mollie.com"
    API_VERSION: str = "v2"
    UNAME: str = " ".join(platform.uname())

    OAUTH_AUTHORIZATION_URL: str = "https://my.mollie.com/oauth2/authorize"
    OAUTH_AUTO_REFRESH_URL: str = API_ENDPOINT + "/oauth2/tokens"
    OAUTH_TOKEN_URL: str = API_ENDPOINT + "/oauth2/tokens"

    _client: requests.Session
    _oauth_client: OAuth2Session
    api_endpoint: str
    api_version: str
    timeout: Union[int, Tuple[int, int]]
    retry: int
    api_key: str = ""
    access_token: str = ""
    user_agent_components: Dict[str, str]
    client_id: str = ""
    client_secret: str = ""
    set_token: Callable[[dict], None]
    testmode: bool = False

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

    def __init__(self, api_endpoint: str = "", timeout: Union[int, Tuple[int, int]] = (2, 10), retry: int = 3) -> None:
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

        # add endpoint resources
        self.payments = Payments(self)
        self.payment_links = PaymentLinks(self)
        self.profiles = Profiles(self)
        self.methods = Methods(self)
        self.refunds = Refunds(self)
        self.chargebacks = Chargebacks(self)
        self.clients = Clients(self)
        self.client_links = ClientLinks(self)
        self.customers = Customers(self)
        self.orders = Orders(self)
        self.organizations = Organizations(self)
        self.invoices = Invoices(self)
        self.permissions = Permissions(self)
        self.onboarding = Onboarding(self)
        self.settlements = Settlements(self)
        self.subscriptions = Subscriptions(self)
        self.balances = Balances(self)
        self.terminals = Terminals(self)

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

    def set_timeout(self, timeout: Union[int, Tuple[int, int]]) -> None:
        self.timeout = timeout

    def set_testmode(self, testmode: bool) -> None:
        self.testmode = testmode

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

    def _format_request_data(
        self,
        path: str,
        data: Optional[Dict[str, Any]],
        params: Optional[Dict[str, Any]],
        http_method: str,
    ) -> Tuple[str, str, Optional[Dict[str, Any]]]:
        if path.startswith(f"{self.api_endpoint}/{self.api_version}"):
            url = path
        else:
            url = f"{self.api_endpoint}/{self.api_version}/{path}"

        payload = ""

        data, params = self._get_testmode(data, params, http_method)

        if data is not None:
            try:
                payload = json.dumps(data)
            except TypeError as err:
                raise RequestSetupError(f"Error encoding data into JSON: {err}.")

        if params is None:
            params = {}

        querystring = generate_querystring(params)
        if querystring:
            url += "?" + querystring
            params = None

        return url, payload, params

    def _get_testmode(self, data, params, http_method):
        if self.testmode or (params and "testmode" in params):
            if not (self.api_key.startswith("access_") or hasattr(self, "_oauth_client")):
                raise RequestSetupError("Configuring testmode only works with access_token or OAuth authorization")

            # Add to params if we're dealing with a GET request, for any other request add to data.
            # If testmode is passed in the params, we're always overriding self.testmode. If
            # self.testmode is True, simply pass in "true".
            if http_method == "GET":
                params["testmode"] = params.get("testmode") or "true"
            elif not data or "testmode" not in data:
                data["testmode"] = params.get("testmode") or True

                # Delete from the params since it's not a valid parameter when the request is not GET
                params.pop("testmode", None)

        return data, params

    def _perform_http_call_apikey(
        self,
        http_method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        idempotency_key: str = "",
    ) -> requests.Response:
        if not self.api_key:
            raise RequestSetupError("You have not set an API key. Please use set_api_key() to set the API key.")

        if not hasattr(self, "_client"):
            self._client = requests.Session()
            self._client.verify = True
            self._setup_retry()

        url, payload, params = self._format_request_data(path, data, params, http_method)
        try:
            headers = {
                "Accept": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": self.user_agent,
                "X-Mollie-Client-Info": self.UNAME,
            }

            if idempotency_key:
                headers.update({"Idempotency-Key": idempotency_key})

            response = self._client.request(
                method=http_method,
                url=url,
                headers=headers,
                params=params,
                data=payload,
                timeout=self.timeout,
            )
        except requests.exceptions.RequestException as err:
            raise RequestError(f"Unable to communicate with Mollie: {err}")

        return response

    def _perform_http_call_oauth(
        self,
        http_method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        idempotency_key: str = "",
    ) -> requests.Response:
        url, payload, params = self._format_request_data(path, data, params, http_method)
        try:
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": self.user_agent,
                "X-Mollie-Client-Info": self.UNAME,
            }

            if idempotency_key:
                headers.update({"Idempotency-Key": idempotency_key})

            response = self._oauth_client.request(
                method=http_method,
                url=url,
                headers=headers,
                params=params,
                data=payload,
                timeout=self.timeout,
            )
        except requests.exceptions.RequestException as err:
            raise RequestError(f"Unable to communicate with Mollie: {err}")
        return response

    def perform_http_call(
        self,
        http_method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        idempotency_key: str = "",
    ) -> requests.Response:
        if hasattr(self, "_oauth_client"):
            return self._perform_http_call_oauth(
                http_method, path, data=data, params=params, idempotency_key=idempotency_key
            )
        else:
            return self._perform_http_call_apikey(
                http_method, path, data=data, params=params, idempotency_key=idempotency_key
            )

    def setup_oauth(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scope: List[str],
        token: str,
        set_token: Callable[[dict], None],
    ) -> Tuple[bool, Optional[str]]:
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

    def setup_oauth_authorization_response(self, authorization_response: str) -> None:
        """
        :param authorization_response: The full callback URL (string)
        :return: None
        """
        # Fetch an OAuth token from the provider using the authorization code obtained during user authorization.
        token = self._oauth_client.fetch_token(
            self.OAUTH_TOKEN_URL,
            authorization_response=authorization_response,
            client_secret=self.client_secret,
        )
        self.set_token(token)

    # TODO Implement https://docs.mollie.com/reference/oauth2/revoke-token
    # def revoke_oauth_token(self, token, type_hint):
    #     ...

    def _setup_retry(self) -> None:
        """Configure a retry behaviour on the HTTP client."""
        if self.retry:
            retry = Retry(connect=self.retry, read=0, backoff_factor=1)
            adapter = requests.adapters.HTTPAdapter(max_retries=retry)

            if hasattr(self, "_client"):
                self._client.mount("https://", adapter)
            elif hasattr(self, "_oauth_client"):
                self._oauth_client.mount("https://", adapter)


def generate_querystring(params: Optional[Dict[str, Any]]) -> Optional[str]:
    """
    Generate a querystring suitable for use in the v2 api.

    The Requests library doesn't know how to generate querystrings that encode dictionaries using square brackets:
    https://api.mollie.com/v2/methods?amount[value]=100.00&amount[currency]=USD
    """
    if not params:
        return None

    parts = []
    for param, value in params.items():
        # TODO clean this up with a simple recursive approach
        if not isinstance(value, dict):
            parts.append(urlencode({param: value}))
        else:
            # encode dictionary with square brackets
            for key, sub_value in value.items():
                composed = f"{param}[{key}]"
                parts.append(urlencode({composed: sub_value}))

    return "&".join(parts)
