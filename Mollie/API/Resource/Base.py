from Mollie.API.Client import *
from Mollie.API.Error import *
from Mollie.API.Object import *

import json


class Base(object):
    REST_CREATE = Client.HTTP_POST
    REST_UPDATE = Client.HTTP_POST
    REST_READ = Client.HTTP_GET
    REST_LIST = Client.HTTP_GET
    REST_DELETE = Client.HTTP_DELETE
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
        result = self.performApiCall(self.REST_READ, path, None, params)
        return self.getResourceObject(result)

    def rest_update(self, resource_id, data, params=None):
        path = self.getResourceName() + '/' + str(resource_id)
        result = self.performApiCall(self.REST_UPDATE, path, data, params)
        return self.getResourceObject(result)

    def rest_delete(self, resource_id, params=None):
        path = self.getResourceName() + '/' + str(resource_id)
        return self.performApiCall(self.REST_DELETE, path, None, params)

    def rest_list(self, params=None):
        path = self.getResourceName()
        result = self.performApiCall(self.REST_LIST, path, None, params)
        return List(result, self.getResourceObject({}).__class__)

    def create(self, data):
        try:
            data = json.dumps(data)
        except Exception as e:
            raise Error('Error encoding parameters into JSON: "%s"' % e.message)
        return self.rest_create(data)

    def get(self, resource_id):
        return self.rest_read(resource_id)

    def update(self, resource_id, data):
        try:
            data = json.dumps(data)
        except Exception as e:
            raise Error('Error encoding parameters into JSON: "%s"' % e.message)
        return self.rest_update(resource_id, data)

    def delete(self, resource_id):
        return self.rest_delete(resource_id)

    def all(self, offset=0, count=DEFAULT_LIMIT):
        return self.rest_list({
            'offset': offset,
            'count': count
        })

    def performApiCall(self, http_method, path, data=None, params=None):
        body = self.client.performHttpCall(http_method, path, data, params)
        try:
            result = body.json()
        except Exception as e:
            raise Error('Unable to decode Mollie response: "%s".' % body)
        if 'error' in result:
            error = Error('Error executing API call (%s): %s.' % (result['error']['type'], result['error']['message']))
            if 'field' in result['error']:
                error.field = result['error']['field']
            raise error
        return result
