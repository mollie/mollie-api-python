from ..objects.organization import Organization
from .base import ResourceBase, ResourceGetMixin

__all__ = [
    "Organizations",
]


class Organizations(ResourceBase, ResourceGetMixin):
    RESOURCE_ID_PREFIX = "org_"

    def get_resource_object(self, result):
        return Organization(result, self.client)

    def get(self, organization_id: str, **params):
        if organization_id != "me":
            self.validate_resource_id(organization_id, "organization ID")
        return super().get(organization_id, **params)
