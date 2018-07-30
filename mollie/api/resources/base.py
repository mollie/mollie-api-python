import json

from mollie.api.error import Error
from mollie.api.objects.list import List


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
                raise Error('Error encoding parameters into JSON: "%s"' % str(e))
        return self.rest_create(data, params)

    def get(self, resource_id, **params):
        return self.rest_read(resource_id, params)

    def update(self, resource_id, data=None, **params):
        if data is not None:
            try:
                data = json.dumps(data)
            except Exception as e:
                raise Error('Error encoding parameters into JSON: "%s"' % str(e))
        return self.rest_update(resource_id, data, params)

    def delete(self, resource_id):
        return self.rest_delete(resource_id)

    def all(self, **params):
        return self.rest_list(params)

    def perform_api_call(self, http_method, path, data=None, params=None):
        body = self.client.perform_http_call(http_method, path, data, params)
        try:
            result = body.json() if body.status_code != 204 else {}
        except Exception:
            raise Error('Unable to decode Mollie response (status code %d): "%s".' % (body.status_code, body.text))
        if 'error' in result:
            error = Error('Error executing API call (%s): %s.' % (result['error']['type'], result['error']['message']))
            if 'field' in result['error']:
                error.field = result['error']['field']
            raise error
        return result
