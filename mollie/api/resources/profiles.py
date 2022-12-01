from typing import Any, Dict, Optional

from ..objects.profile import Profile
from .base import ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin

__all__ = [
    "Profiles",
]


class Profiles(ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin):
    """Resource handler for the `/profiles` endpoint."""

    RESOURCE_ID_PREFIX: str = "pfl_"

    def get_resource_object(self, result: dict) -> Profile:
        return Profile(result, self.client)

    def get(self, resource_id: str, **params: Any) -> Profile:
        if resource_id != "me":
            self.validate_resource_id(resource_id, "profile ID")
        return super().get(resource_id, **params)

    def delete(self, resource_id: str, **params: Any) -> dict:
        self.validate_resource_id(resource_id, "profile ID")
        return super().delete(resource_id, **params)

    def update(self, resource_id: str, data: Optional[Dict[str, Any]] = None, **params: Any) -> Profile:
        self.validate_resource_id(resource_id, "profile ID")
        return super().update(resource_id, **params)
