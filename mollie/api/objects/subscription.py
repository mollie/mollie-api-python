from .base import ObjectBase


class Subscription(ObjectBase):
    @classmethod
    def get_resource_class(cls, client):
        from ..resources.customer_subscriptions import CustomerSubscriptions

        return CustomerSubscriptions(client)

    STATUS_ACTIVE = "active"
    STATUS_PENDING = "pending"  # Waiting for a valid mandate.
    STATUS_CANCELED = "canceled"
    STATUS_SUSPENDED = "suspended"  # Active, but mandate became invalid.
    STATUS_COMPLETED = "completed"

    @property
    def status(self):
        return self._get_property("status")

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
        return self._get_property("resource")

    @property
    def id(self):
        return self._get_property("id")

    @property
    def mode(self):
        return self._get_property("mode")

    @property
    def created_at(self):
        return self._get_property("createdAt")

    @property
    def amount(self):
        return self._get_property("amount")

    @property
    def times(self):
        return int(self._get_property("times"))

    @property
    def times_remaining(self):
        return int(self._get_property("timesRemaining"))

    @property
    def interval(self):
        return self._get_property("interval")

    @property
    def start_date(self):
        return self._get_property("startDate")

    @property
    def next_payment_date(self):
        return self._get_property("nextPaymentDate")

    @property
    def description(self):
        return self._get_property("description")

    @property
    def method(self):
        return self._get_property("method")

    @property
    def mandate_id(self):
        return self._get_property("mandateId")

    @property
    def canceled_at(self):
        return self._get_property("canceledAt")

    @property
    def webhook_url(self):
        return self._get_property("webhookUrl")

    @property
    def metadata(self):
        return self._get_property("metadata")

    @property
    def application_fee(self):
        return self._get_property("applicationFee")

    @property
    def customer(self):
        """Return the customer for this subscription."""
        url = self._get_link("customer")
        return self.client.customers.from_url(url)

    @property
    def profile(self):
        """Return the profile related to this subscription."""
        url = self._get_link("profile")
        if not url:
            return None
        return self.client.profiles.from_url(url)

    @property
    def payments(self):
        """Return a list of payments for this subscription."""
        payments = self.client.subscription_payments.on(self).list()
        return payments

    # TODO: Implement this property.
    # Payload from API is missing customerId or a _links['mandate'] field to do this efficiently.
    # @property
    # def mandate(self):
    #     pass
