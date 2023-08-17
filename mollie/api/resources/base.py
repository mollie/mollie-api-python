import logging
import uuid
from typing import TYPE_CHECKING, Any, Dict, Optional, Type

from mollie.api.objects.base import ObjectBase

from ..error import IdentifierError, ResponseError, ResponseHandlingError
from ..objects.list import PaginationList

if TYPE_CHECKING:
    from ..client import Client


class ResourceBase:
    DEFAULT_LIMIT = 10

    REST_CREATE: str = "POST"
    REST_READ: str = "GET"
    REST_LIST: str = "GET"
    REST_UPDATE: str = "PATCH"
    REST_DELETE: str = "DELETE"

    RESOURCE_ID_PREFIX: str = ""

    object_type: Type[ObjectBase]

    def __init__(self, client: "Client") -> None:
        self.client = client

    def get_resource_path(self) -> str:
        """Return the base URL path in the API for this resource."""
        return self.__class__.__name__.lower()

    def perform_api_call(
        self,
        http_method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        idempotency_key: str = "",
    ) -> Dict[str, Any]:
        resp = self.client.perform_http_call(http_method, path, data, params, idempotency_key)
        if "application/hal+json" in resp.headers.get("Content-Type", ""):
            # set the content type according to the media type definition
            resp.encoding = "utf-8"
        try:
            result = resp.json() if resp.status_code != 204 else {}
        except Exception:
            raise ResponseHandlingError(
                f"Unable to decode Mollie API response (status code: {resp.status_code}): '{resp.text}'.",
                idempotency_key,
            )
        if resp.status_code < 200 or resp.status_code > 299:
            if "status" in result and (result["status"] < 200 or result["status"] > 299):
                # the factory will return the appropriate ResponseError subclass based on the result
                raise ResponseError.factory(result, idempotency_key)
            else:
                raise ResponseHandlingError(
                    "Received HTTP error from Mollie API, but no status in payload "
                    f"(status code: {resp.status_code}): '{resp.text}'.",
                    idempotency_key,
                )
        if resp.headers.get("Idempotent-Replayed"):
            logging.warning(
                f"The 'Idempotent-Replayed' header was set in the API response, the Idempotency-Key used in the "
                f"request was '{idempotency_key}'. See https://docs.mollie.com/overview/api-idempotency for details"
            )

        return result

    @classmethod
    def validate_resource_id(cls, resource_id: str, name: str = "Identifier", message: str = "") -> None:
        """Generic identifier validation."""
        if not message:
            message = f"Invalid {name} '{resource_id}', it should start with '{cls.RESOURCE_ID_PREFIX}'."

        if not resource_id or not str(resource_id).startswith(cls.RESOURCE_ID_PREFIX):
            raise IdentifierError(message)

    @staticmethod
    def _generate_idempotency_key() -> str:
        return str(uuid.uuid4())


class ResourceCreateMixin(ResourceBase):
    def create(self, data: Optional[Dict[str, Any]] = None, idempotency_key: str = "", **params: Any) -> Any:
        idempotency_key = idempotency_key or self._generate_idempotency_key()
        path = self.get_resource_path()
        result = self.perform_api_call(self.REST_CREATE, path, data, params, idempotency_key=idempotency_key)
        return self.object_type(result, self.client)


class ResourceGetMixin(ResourceBase):
    def get(self, resource_id: str, **params: Any) -> Any:
        resource_path = self.get_resource_path()
        path = f"{resource_path}/{resource_id}"
        result = self.perform_api_call(self.REST_READ, path, params=params)
        return self.object_type(result, self.client)

    def from_url(self, url: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Utility method to return an object from a full URL (such as from _links).

        This method always does a GET request and returns a single Object.
        """
        result = self.perform_api_call(self.REST_READ, url, params=params)
        return self.object_type(result, self.client)


class ResourceListMixin(ResourceBase):
    def list(self, **params: Any) -> PaginationList:
        path = self.get_resource_path()
        result = self.perform_api_call(self.REST_LIST, path, params=params)
        return PaginationList(result, self, self.client)


class ResourceUpdateMixin(ResourceBase):
    def update(
        self, resource_id: str, data: Optional[Dict[str, Any]] = None, idempotency_key: str = "", **params: Any
    ) -> Any:
        idempotency_key = idempotency_key or self._generate_idempotency_key()
        resource_path = self.get_resource_path()
        path = f"{resource_path}/{resource_id}"
        result = self.perform_api_call(self.REST_UPDATE, path, data, params, idempotency_key=idempotency_key)
        return self.object_type(result, self.client)


class ResourceDeleteMixin(ResourceBase):
    def delete(self, resource_id: str, idempotency_key: str = "", **params: Any) -> Any:
        idempotency_key = idempotency_key or self._generate_idempotency_key()
        resource_path = self.get_resource_path()
        path = f"{resource_path}/{resource_id}"
        return self.perform_api_call(self.REST_DELETE, path, params=params, idempotency_key=idempotency_key)
