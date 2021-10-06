from typing import TYPE_CHECKING, Any, Callable, Optional, Tuple

if TYPE_CHECKING:
    import requests
    import requests_oauthlib

    from .typing import Timeout


class Client:
    access_token: Optional[dict[Any, Any]]
    api_key: Optional[str]
    client_secret = Optional[str]
    set_token: Optional[Callable[[str], None]]
    user_agent_components: dict[str, str]
    _client: Optional[requests.Session]
    _oauth_client: Optional[requests_oauthlib.OAuth2Session]

    @staticmethod
    def validate_api_endpoint(api_endpoint: str) -> str:
        ...

    @staticmethod
    def validate_api_key(api_key: str) -> str:
        ...

    @staticmethod
    def validate_access_token(access_token: str) -> str:
        ...

    def __init__(self, api_endpoint: Optional[str] = None, timeout: Timeout = (2, 10), retry: int = 3):
        ...

    def set_api_endpoint(self, api_endpoint: str) -> None:
        ...

    def set_api_key(self, api_key: str) -> None:
        ...

    def set_timeout(self, timeout: Timeout) -> None:
        ...

    def set_user_agent_component(self, key: str, value: str, sanitize: bool = True) -> None:
        ...

    def user_agent(self) -> str:
        ...

    def _format_request_data(
        self, path: str, data: Any, params: Optional[dict[str, Any]]
    ) -> tuple[str, Optional[str], Optional[dict[str, Any]]]:
        ...

    def _perform_http_call_apikey(
        self,
        http_method: str,
        path: str,
        data: Any = None,
        params: Optional[dict[Any, Any]] = None,
    ) -> requests.Response:
        ...

    def _perform_http_call_oauth(
        self,
        http_method: str,
        path: str,
        data: Any = None,
        params: Optional[dict[Any, Any]] = None,
    ) -> requests.Response:
        ...

    def perform_http_call(
        self,
        http_method: str,
        path: str,
        data: Optional[dict[Any, Any]] = None,
        params: Optional[dict[Any, Any]] = None,
    ) -> requests.Response:
        ...

    def setup_oauth(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scope: Tuple[str, ...],
        token: dict[Any, Any],
        set_token: Callable[[str], None],
    ) -> tuple[Any, Optional[Any]]:
        ...

    def setup_oauth_authorization_response(self, authorization_response: str) -> dict[Any, Any]:
        ...

    def _setup_retry(self) -> None:
        ...


def generate_querystring(params: Optional[dict[Any, Any]]) -> Optional[str]:
    ...
