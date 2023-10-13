from typing import Any

from ..objects.organization import Organization
from .base import ResourceGetMixin

__all__ = [
    "Organizations",
]


class Organizations(ResourceGetMixin):
    """Resource handler for the `/organizations` endpoint."""

    RESOURCE_ID_PREFIX: str = "org_"
    object_type = Organization

    def get(self, resource_id: str, **params: Any) -> Organization:
        if resource_id != "me":
            self.validate_resource_id(resource_id, "organization ID")
        return super().get(resource_id, **params)
