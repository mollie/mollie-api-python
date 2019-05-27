from .base import Base


class Permission(Base):
    @classmethod
    def get_resource_class(cls, client):
        from ..resources.permissions import Permissions
        return Permissions(client)

    @property
    def id(self):
        return self._get_property('id')

    @property
    def resource(self):
        return self._get_property('resource')

    @property
    def description(self):
        return self._get_property('description')

    @property
    def granted(self):
        return self._get_property('granted')
