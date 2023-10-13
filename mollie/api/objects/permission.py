from .base import ObjectBase


class Permission(ObjectBase):
    @property
    def id(self):
        return self._get_property("id")

    @property
    def resource(self):
        return self._get_property("resource")

    @property
    def description(self):
        return self._get_property("description")

    @property
    def granted(self):
        return self._get_property("granted")
