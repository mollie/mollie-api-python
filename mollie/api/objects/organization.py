from .base import Base


class Organization(Base):
    @classmethod
    def get_resource_class(cls, client):
        from ..resources.organizations import Organizations
        return Organizations(client)

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
    def address(self):
        return self._get_property('address')

    @property
    def registration_number(self):
        return self._get_property('registrationNumber')

    @property
    def vat_number(self):
        return self._get_property('vatNumber')

    @property
    def dashboard(self):
        return self._get_link('dashboard')
