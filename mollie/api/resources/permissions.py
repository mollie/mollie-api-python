import re
from typing import Any

from ..error import IdentifierError
from ..objects.permission import Permission
from .base import ResourceGetMixin, ResourceListMixin

__all__ = [
    "Permissions",
]


class Permissions(ResourceGetMixin, ResourceListMixin):
    """Resource handler for the `/permissions` endpoint."""

    object_type = Permission

    @staticmethod
    def validate_permission_id(permission_id: str) -> None:
        if not permission_id or not bool(re.match(r"^[a-z]+\.[a-z]+$", permission_id)):
            raise IdentifierError(f"Invalid permission ID: '{permission_id}'. Does not match ^[a-z]+.[a-z]+$")

    def get(self, resource_id: str, **params: Any) -> Permission:
        self.validate_resource_id(resource_id)
        return super().get(resource_id, **params)
