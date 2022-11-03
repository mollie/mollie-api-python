from typing import Optional

from ..error import IdentifierError, ResponseError, ResponseHandlingError
from ..objects.list import ObjectList


class ResourceBase(object):
    DEFAULT_LIMIT = 10

    REST_CREATE = "POST"
    REST_READ = "GET"
    REST_LIST = "GET"
    REST_UPDATE = "PATCH"
    REST_DELETE = "DELETE"

    def __init__(self, client):
        self.client = client

    def get_resource_object(self, result: dict):
        """
        Return an instantiated result class for this resource. Should be overriden by a subclass.

        :param result: The API response that the object should hold.
        :type result: dict
        """
        raise NotImplementedError()  # pragma: no cover

    def get_resource_path(self):
        """Return the base URL path in the API for this resource."""
        return self.__class__.__name__.lower()

    def perform_api_call(self, http_method, path, data=None, params=None):
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
    def validate_resource_id(cls, resource_id: str, name: str = "Identifier", message: str = ""):
        """Generic identifier validation."""
        if not message:
            message = f"Invalid {name} '{resource_id}', it should start with '{cls.RESOURCE_ID_PREFIX}'."

        if not resource_id or not str(resource_id).startswith(cls.RESOURCE_ID_PREFIX):
            raise IdentifierError(message)

    @staticmethod
    def extract_embed(params):
        """Extract and parse the embed parameter from the request."""
        # TODO Remove this
        if "embed" not in params:
            return
        return params["embed"].split(",")


class ResourceCreateMixin:
    def create(self, data=None, **params):
        path = self.get_resource_path()
        result = self.perform_api_call(self.REST_CREATE, path, data, params)
        return self.get_resource_object(result)


class ResourceGetMixin:
    def get(self, resource_id: str, **params):
        resource_path = self.get_resource_path()
        path = f"{resource_path}/{resource_id}"
        result = self.perform_api_call(self.REST_READ, path, params=params)
        return self.get_resource_object(result)

    def from_url(self, url, data=None, params=None):
        """Utility method to return an object from a full URL (such as from _links).

        This method always does a GET request and returns a single Object.
        """
        result = self.perform_api_call(self.REST_READ, url, data, params)
        return self.get_resource_object(result)


class ResourceListMixin:
    def list(self, **params):
        path = self.get_resource_path()
        result = self.perform_api_call(self.REST_LIST, path, params=params)
        return ObjectList(result, self.get_resource_object({}).__class__, self.client)


class ResourceUpdateMixin:
    def update(self, resource_id: str, data=None, **params):
        resource_path = self.get_resource_path()
        path = f"{resource_path}/{resource_id}"
        result = self.perform_api_call(self.REST_UPDATE, path, data, params)
        return self.get_resource_object(result)


class ResourceDeleteMixin:
    def delete(self, resource_id: str, **params: Optional[dict]):
        resource_path = self.get_resource_path()
        path = f"{resource_path}/{resource_id}"
        return self.perform_api_call(self.REST_DELETE, path, params=params)
