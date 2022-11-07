from ..objects.organization import Organization
from .base import ResourceGetMixin

__all__ = [
    "Organizations",
]


class Organizations(ResourceGetMixin):
    """Resource handler for the `/organizations` endpoint."""

    RESOURCE_ID_PREFIX = "org_"

    def get_resource_object(self, result: dict) -> Organization:
        return Organization(result, self.client)

    def get(self, resource_id: str, **params):
        if resource_id != "me":
            self.validate_resource_id(resource_id, "organization ID")
        return super().get(resource_id, **params)
