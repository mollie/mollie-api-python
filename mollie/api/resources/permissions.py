import re

from ..error import IdentifierError
from ..objects.permission import Permission
from .base import ResourceBase


class Permissions(ResourceBase):
    def get_resource_object(self, result):
        return Permission(result, self.client)

    @staticmethod
    def validate_permission_id(permission_id):
        if not permission_id or not bool(re.match(r"^[a-z]+\.[a-z]+$", permission_id)):
            raise IdentifierError(f"Invalid permission ID: '{permission_id}'. Does not match ^[a-z]+.[a-z]+$")

    def get(self, permission_id, **params):
        self.validate_permission_id(permission_id)
        return super().get(permission_id, **params)
