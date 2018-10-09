from .base import Base
from .list import List


class Customer(Base):
    @classmethod
    def get_resource_class(cls, client):
        from ..resources.customers import Customers
        return Customers(client)

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
        """Return the subscription list for the customer."""
        from .subscription import Subscription
        url = self._get_link('subscriptions')
        if url:
            resp = self._resource.perform_api_call(self._resource.REST_READ, url)
            return List(resp, Subscription)

    @property
    def mandates(self):
        """Return the mandate list for the customer."""
        from .mandate import Mandate  # work around circular import
        url = self._get_link('mandates')
        if url:
            resp = self._resource.perform_api_call(self._resource.REST_READ, url)
            return List(resp, Mandate)

    @property
    def payments(self):
        """Return the payment list for the customer."""
        from .payment import Payment  # work around circular import
        url = self._get_link('payments')
        if url:
            resp = self._resource.perform_api_call(self._resource.REST_READ, url)
            return List(resp, Payment)
