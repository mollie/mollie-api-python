from .base import ObjectBase


class Organization(ObjectBase):
    @property
    def id(self):
        return self._get_property("id")

    @property
    def resource(self):
        return self._get_property("resource")

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
    def address(self):
        return self._get_property("address")

    @property
    def registration_number(self):
        return self._get_property("registrationNumber")

    @property
    def vat_number(self):
        return self._get_property("vatNumber")

    @property
    def vat_regulation(self):
        return self._get_property("vatRegulation")

    @property
    def dashboard(self):
        return self._get_link("dashboard")

    # TODO: Implement https://docs.mollie.com/reference/v2/organizations-api/get-partner
    # def get_partner(self):
    #     ...
