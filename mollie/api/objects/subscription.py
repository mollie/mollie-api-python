import re

from .base import ObjectBase
from .customer import Customer


class Subscription(ObjectBase):
    @classmethod
    def get_resource_class(cls, client):
        from ..resources import CustomerSubscriptions

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

    def get_customer(self):
        """Return the customer for this subscription."""
        url = self._get_link("customer")
        return self.client.customers.from_url(url)

    @property
    def customer_id(self):
        """
        Retrieve the customer id from the customer link.

        The customer_id is not available as a direct subscription property,
        but we need it to implement various features that need it. The only
        option is to extract it from the link.
        """
        url = self._get_link("customer")
        matches = re.findall(r"/customers/(cst_\w+)", url)
        if matches:
            return matches[0]

    def get_profile(self):
        """Return the profile related to this subscription."""
        url = self._get_link("profile")
        if not url:
            return None
        return self.client.profiles.from_url(url)

    def get_mandate(self):
        if self.mandate_id and self.customer_id:
            from ..resources import CustomerMandates

            customer = Customer({"id": self.customer_id}, self.client)
            return CustomerMandates(self.client, customer).get(self.mandate_id)

    @property
    def payments(self):
        # We could also have implemented this using the "payments" entry from the _links, but then we would not have
        # the explicit interface using .payments.list()
        from ..resources import SubscriptionPayments

        customer = Customer({"id": self.customer_id}, self.client)
        return SubscriptionPayments(self.client, customer=customer, subscription=self)
