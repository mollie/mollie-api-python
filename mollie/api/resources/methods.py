from ..objects.list import List
from ..objects.method import Method
from .base import Base


class Methods(Base):
    def get_resource_object(self, result):
        return Method(result)

    def all(self, **params):
        """List all mollie payment methods, including methods that aren't activated in your profile."""
        path = 'methods/all'
        result = self.perform_api_call(self.REST_LIST, path, params=params)
        return List(result, self.get_resource_object({}).__class__, self.client)
