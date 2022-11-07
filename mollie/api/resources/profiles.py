from typing import Optional

from ..objects.profile import Profile
from .base import ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin

__all__ = [
    "Profiles",
]


class Profiles(ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin):
    """Resource handler for the `/profiles` endpoint."""

    RESOURCE_ID_PREFIX = "pfl_"

    def get_resource_object(self, result: dict) -> Profile:
        return Profile(result, self.client)

    def get(self, resource_id: str, **params):
        if resource_id != "me":
            self.validate_resource_id(resource_id, "profile ID")
        return super().get(resource_id, **params)

    def delete(self, resource_id: str, **params):
        self.validate_resource_id(resource_id, "profile ID")
        return super().delete(resource_id, **params)

    def update(self, resource_id: str, data: Optional[dict] = None, **params):
        self.validate_resource_id(resource_id, "profile ID")
        return super().update(resource_id, **params)
