from .base import ObjectBase


class Customer(ObjectBase):
    @classmethod
    def get_resource_class(cls, client):
        from ..resources import Customers

        return Customers(client)

    @property
    def id(self):
        return self._get_property("id")

    @property
    def name(self):
        return self._get_property("name")

    @property
    def email(self):
        return self._get_property("email")

    @property
    def locale(self):
        return self._get_property("locale")

    @property
    def metadata(self):
        return self._get_property("metadata")

    @property
    def mode(self):
        return self._get_property("mode")

    @property
    def resource(self):
        return self._get_property("resource")

    @property
    def created_at(self):
        return self._get_property("createdAt")

    @property
    def subscriptions(self):
        from ..resources import CustomerSubscriptions

        return CustomerSubscriptions(self.client, self)

    @property
    def mandates(self):
        from ..resources import CustomerMandates

        return CustomerMandates(self.client, self)

    @property
    def payments(self):
        from ..resources import CustomerPayments

        return CustomerPayments(self.client, self)
