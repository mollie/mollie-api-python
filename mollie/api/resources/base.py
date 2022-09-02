from ..error import ResponseError, ResponseHandlingError
from ..objects.list import ObjectList


class ResourceBase(object):
    DEFAULT_LIMIT = 10

    def __init__(self, client):
        self.client = client

    def get_resource_object(self, result):
        raise NotImplementedError()  # pragma: no cover

    def get_resource_name(self):
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

    @staticmethod
    def extract_embed(params):
        """Extract and parse the embed parameter from the request."""
        if "embed" not in params:
            return
        return params["embed"].split(",")


class ResourceCreateMixin:
    REST_CREATE = "POST"

    def create(self, data=None, **params):
        path = self.get_resource_name()
        result = self.perform_api_call(self.REST_CREATE, path, data, params)
        return self.get_resource_object(result)


class ResourceGetMixin:
    REST_READ = "GET"

    def get(self, resource_id, **params):
        path = self.get_resource_name() + "/" + str(resource_id)
        result = self.perform_api_call(self.REST_READ, path, params=params)
        return self.get_resource_object(result)

    def from_url(self, url, data=None, params=None):
        """Utility method to return an object from a full URL (such as from _links).

        This method always does a GET request and returns a single Object.
        """
        result = self.perform_api_call(self.REST_READ, url, data, params)
        return self.get_resource_object(result)


class ResourceListMixin:
    REST_LIST = "GET"

    def list(self, **params):
        path = self.get_resource_name()
        result = self.perform_api_call(self.REST_LIST, path, params=params)
        return ObjectList(result, self.get_resource_object({}).__class__, self.client)


class ResourceUpdateMixin:
    REST_UPDATE = "PATCH"

    def update(self, resource_id, data=None, **params):
        path = self.get_resource_name() + "/" + str(resource_id)
        result = self.perform_api_call(self.REST_UPDATE, path, data, params)
        return self.get_resource_object(result)


class ResourceDeleteMixin:
    REST_DELETE = "DELETE"

    def delete(self, resource_id, data=None):
        path = self.get_resource_name() + "/" + str(resource_id)
        return self.perform_api_call(self.REST_DELETE, path, data)


class ResourceAllMethodsMixin(
    ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin
):
    pass
