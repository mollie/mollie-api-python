import json

from ..error import RequestSetupError, ResponseError, ResponseHandlingError
from ..objects.list import List


class Base(object):
    REST_CREATE = 'POST'
    REST_UPDATE = 'PATCH'
    REST_READ = 'GET'
    REST_LIST = 'GET'
    REST_DELETE = 'DELETE'
    DEFAULT_LIMIT = 10

    def __init__(self, client):
        self.client = client

    def get_resource_object(self, result):
        raise NotImplementedError()

    def get_resource_name(self):
        return self.__class__.__name__.lower()

    def rest_create(self, data, params=None):
        path = self.get_resource_name()
        result = self.perform_api_call(self.REST_CREATE, path, data, params)
        return self.get_resource_object(result)

    def rest_read(self, resource_id, params=None):
        path = self.get_resource_name() + '/' + str(resource_id)
        result = self.perform_api_call(self.REST_READ, path, params=params)
        return self.get_resource_object(result)

    def rest_update(self, resource_id, data, params=None):
        path = self.get_resource_name() + '/' + str(resource_id)
        result = self.perform_api_call(self.REST_UPDATE, path, data, params)
        return self.get_resource_object(result)

    def rest_delete(self, resource_id, params=None):
        path = self.get_resource_name() + '/' + str(resource_id)
        return self.perform_api_call(self.REST_DELETE, path, params=params)

    def rest_list(self, params=None):
        path = self.get_resource_name()
        result = self.perform_api_call(self.REST_LIST, path, params=params)
        return List(result, self.get_resource_object({}).__class__)

    def create(self, data=None, **params):
        if data is not None:
            try:
                data = json.dumps(data)
            except Exception as e:
                raise RequestSetupError('Error encoding parameters into JSON: "%s"' % str(e))
        return self.rest_create(data, params)

    def get(self, resource_id, **params):
        return self.rest_read(resource_id, params)

    def update(self, resource_id, data=None, **params):
        if data is not None:
            try:
                data = json.dumps(data)
            except Exception as e:
                raise RequestSetupError('Error encoding parameters into JSON: "%s"' % str(e))
        return self.rest_update(resource_id, data, params)

    def delete(self, resource_id):
        return self.rest_delete(resource_id)

    def list(self, **params):
        return self.rest_list(params)

    def perform_api_call(self, http_method, path, data=None, params=None):
        resp = self.client.perform_http_call(http_method, path, data, params)
        try:
            result = resp.json() if resp.status_code != 204 else {}
        except Exception:
            raise ResponseHandlingError('Unable to decode Mollie API response (status code: %d): %s' % (
                resp.status_code, resp.text))
        if resp.status_code < 200 or resp.status_code > 299:
            if 'status' in result and (result['status'] < 200 or result['status'] > 299):
                # the factory will return the appropriate ResponseError subclass based on the result
                raise ResponseError.factory(result)
            else:
                raise ResponseHandlingError(
                    'Received HTTP error from Mollie API, but no status in payload (status code: %d): %s' % (
                        resp.status_code, resp.text))
        return result
