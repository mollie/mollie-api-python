from .base import Base
from .customer import Customer


class Subscription(Base):
    @classmethod
    def get_resource_class(cls, client):
        from ..resources.customer_subscriptions import CustomerSubscriptions
        return CustomerSubscriptions(client)

    STATUS_ACTIVE = 'active'
    STATUS_PENDING = 'pending'   # Waiting for a valid mandate.
    STATUS_CANCELED = 'canceled'
    STATUS_SUSPENDED = 'suspended'  # Active, but mandate became invalid.
    STATUS_COMPLETED = 'completed'

    @property
    def status(self):
        return self._get_property('status')

    def is_active(self):
        return self.status == self.STATUS_ACTIVE

    def is_pending(self):
        return self.status == self.STATUS_PENDING

    def is_canceled(self):
        return self.status == self.STATUS_CANCELED

    def is_suspended(self):
        return self.status == self.STATUS_SUSPENDED

    def is_completed(self):
        return self.status == self.STATUS_COMPLETED

    @property
    def resource(self):
        return self._get_property('resource')

    @property
    def id(self):
        return self._get_property('id')

    @property
    def mode(self):
        return self._get_property('mode')

    @property
    def created_at(self):
        return self._get_property('createdAt')

    @property
    def amount(self):
        return self._get_property('amount')

    @property
    def times(self):
        return int(self._get_property('times'))

    @property
    def interval(self):
        return self._get_property('interval')

    @property
    def start_date(self):
        return self._get_property('startDate')

    @property
    def description(self):
        return self._get_property('description')

    @property
    def method(self):
        return self._get_property('method')

    @property
    def canceled_at(self):
        return self._get_property('canceledAt')

    @property
    def webhook_url(self):
        return self._get_property('webhookUrl')

    @property
    def customer(self):
        """Return the customer for this subscription."""
        url = self._get_link('customer')
        if url:
            resp = self._resource.perform_api_call(self._resource.REST_READ, url)
            return Customer(resp)
