import re

from ..error import IdentifierError
from ..objects.permission import Permission
from .base import ResourceGetMixin, ResourceListMixin

__all__ = [
    "Permissions",
]


class Permissions(ResourceGetMixin, ResourceListMixin):
    """Resource handler for the `/permissions` endpoint."""

    def get_resource_object(self, result: dict) -> Permission:
        return Permission(result, self.client)

    @staticmethod
    def validate_permission_id(permission_id: str):
        # TODO Maybe we should just include a list of supported permissions?
        if not permission_id or not bool(re.match(r"^[a-z]+\.[a-z]+$", permission_id)):
            raise IdentifierError(f"Invalid permission ID: '{permission_id}'. Does not match ^[a-z]+.[a-z]+$")

    def get(self, resource_id: str, **params):
        self.validate_resource_id(resource_id)
        return super().get(resource_id, **params)
