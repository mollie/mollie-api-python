import json

from Mollie.API import Error
from Mollie.API.Object import List


class Base(object):
    REST_CREATE = 'POST'
    REST_UPDATE = 'POST'
    REST_READ = 'GET'
    REST_LIST = 'GET'
    REST_DELETE = 'DELETE'
    DEFAULT_LIMIT = 10

    def __init__(self, client):
        self.client = client

    def getResourceObject(self, result):
        raise NotImplementedError()

    def getResourceName(self):
        return self.__class__.__name__.lower()

    def rest_create(self, data, params=None):
        path = self.getResourceName()
        result = self.performApiCall(self.REST_CREATE, path, data, params)
        return self.getResourceObject(result)

    def rest_read(self, resource_id, params=None):
        path = self.getResourceName() + '/' + str(resource_id)
        result = self.performApiCall(self.REST_READ, path, params=params)
        return self.getResourceObject(result)

    def rest_update(self, resource_id, data, params=None):
        path = self.getResourceName() + '/' + str(resource_id)
        result = self.performApiCall(self.REST_UPDATE, path, data, params)
        return self.getResourceObject(result)

    def rest_delete(self, resource_id, params=None):
        path = self.getResourceName() + '/' + str(resource_id)
        return self.performApiCall(self.REST_DELETE, path, params=params)

    def rest_list(self, params=None):
        path = self.getResourceName()
        result = self.performApiCall(self.REST_LIST, path, params=params)
        return List(result, self.getResourceObject({}).__class__)

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

    def performApiCall(self, http_method, path, data=None, params=None):
        body = self.client.performHttpCall(http_method, path, data, params)
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
