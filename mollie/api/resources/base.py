from typing import Any, Optional

from ..error import IdentifierError, ResponseError, ResponseHandlingError
from ..objects.list import ObjectList


class ResourceBase:
    DEFAULT_LIMIT = 10

    REST_CREATE: str = "POST"
    REST_READ: str = "GET"
    REST_LIST: str = "GET"
    REST_UPDATE: str = "PATCH"
    REST_DELETE: str = "DELETE"

    RESOURCE_ID_PREFIX: str = ""

    def __init__(self, client):
        self.client = client

    def get_resource_object(self, result: dict) -> Any:
        """
        Return an instantiated result class for this resource. Should be overriden by a subclass.

        :param result: The API response that the object should hold.
        :type result: dict
        """
        raise NotImplementedError()  # pragma: no cover

    def get_resource_path(self) -> str:
        """Return the base URL path in the API for this resource."""
        return self.__class__.__name__.lower()

    def perform_api_call(
        self, http_method: str, path: str, data: Optional[dict] = None, params: Optional[dict] = None
    ) -> dict:
        resp = self.client.perform_http_call(http_method, path, data, params)
        if "application/hal+json" in resp.headers.get("Content-Type", ""):
            # set the content type according to the media type definition
            resp.encoding = "utf-8"
        try:
            result = resp.json() if resp.status_code != 204 else {}
        except Exception:
            raise ResponseHandlingError(
                f"Unable to decode Mollie API response (status code: {resp.status_code}): '{resp.text}'."
            )
        if resp.status_code < 200 or resp.status_code > 299:
            if "status" in result and (result["status"] < 200 or result["status"] > 299):
                # the factory will return the appropriate ResponseError subclass based on the result
                raise ResponseError.factory(result)
            else:
                raise ResponseHandlingError(
                    "Received HTTP error from Mollie API, but no status in payload "
                    f"(status code: {resp.status_code}): '{resp.text}'."
                )
        return result

    @classmethod
    def validate_resource_id(cls, resource_id: str, name: str = "Identifier", message: Optional[str] = None) -> None:
        """Generic identifier validation."""
        if not message:
            message = f"Invalid {name} '{resource_id}', it should start with '{cls.RESOURCE_ID_PREFIX}'."

        if not resource_id or not str(resource_id).startswith(cls.RESOURCE_ID_PREFIX):
            raise IdentifierError(message)


class ResourceCreateMixin(ResourceBase):
    def create(self, data: Optional[dict] = None, **params):
        path = self.get_resource_path()
        result = self.perform_api_call(self.REST_CREATE, path, data, params)
        return self.get_resource_object(result)


class ResourceGetMixin(ResourceBase):
    def get(self, resource_id: str, **params):
        resource_path = self.get_resource_path()
        path = f"{resource_path}/{resource_id}"
        result = self.perform_api_call(self.REST_READ, path, params=params)
        return self.get_resource_object(result)

    def from_url(self, url: str, data: Optional[dict] = None, params: Optional[dict] = None):
        """Utility method to return an object from a full URL (such as from _links).

        This method always does a GET request and returns a single Object.
        """
        result = self.perform_api_call(self.REST_READ, url, data, params)
        return self.get_resource_object(result)


class ResourceListMixin(ResourceBase):
    def list(self, **params):
        path = self.get_resource_path()
        result = self.perform_api_call(self.REST_LIST, path, params=params)
        return ObjectList(result, self.get_resource_object({}).__class__, self.client)


class ResourceUpdateMixin(ResourceBase):
    def update(self, resource_id: str, data: Optional[dict] = None, **params):
        resource_path = self.get_resource_path()
        path = f"{resource_path}/{resource_id}"
        result = self.perform_api_call(self.REST_UPDATE, path, data, params)
        return self.get_resource_object(result)


class ResourceDeleteMixin(ResourceBase):
    def delete(self, resource_id: str, **params):
        resource_path = self.get_resource_path()
        path = f"{resource_path}/{resource_id}"
        return self.perform_api_call(self.REST_DELETE, path, params=params)
