from .base import Base
from .list import List


class Customer(Base):
    @property
    def id(self):
        return self._get_property('id')

    @property
    def name(self):
        return self._get_property('name')

    @property
    def email(self):
        return self._get_property('email')

    @property
    def locale(self):
        return self._get_property('locale')

    @property
    def metadata(self):
        return self._get_property('metadata')

    @property
    def mode(self):
        return self._get_property('mode')

    @property
    def resource(self):
        return self._get_property('resource')

    @property
    def created_at(self):
        return self._get_property('createdAt')

    @property
    def subscriptions(self):
        """Return subscription object from the links attribute"""
        from .subscription import Subscription
        try:
            url = self['_links']['subscriptions']['href']
        except KeyError:
            return None
        resp = self._resource.perform_api_call(self._resource.REST_READ, url)
        return List(resp, Subscription)

    @property
    def mandates(self):
        """Return the mandate list referenced in the _links."""
        from .mandate import Mandate  # work around circular import
        try:
            url = self['_links']['mandates']['href']
        except KeyError:
            return None
        resp = self._resource.perform_api_call(self._resource.REST_READ, url)
        return List(resp, Mandate)
