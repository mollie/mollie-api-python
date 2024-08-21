from .base import ObjectBase


class Terminal(ObjectBase):
    @property
    def id(self):
        return self._get_property("id")

    @property
    def status(self):
        return self._get_property("status")

    @property
    def brand(self):
        return self._get_property("brand")

    @property
    def model(self):
        return self._get_property("model")

    @property
    def serial_number(self):
        return self._get_property("serialNumber")

    @property
    def currency(self):
        return self._get_property("currency")

    @property
    def description(self):
        return self._get_property("description")

    @property
    def profile_id(self):
        return self._get_property("profileId")

    @property
    def created_at(self):
        return self._get_property("createdAt")
