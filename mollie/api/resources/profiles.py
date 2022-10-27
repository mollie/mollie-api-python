from ..objects.profile import Profile
from .base import (
    ResourceBase,
    ResourceCreateMixin,
    ResourceDeleteMixin,
    ResourceGetMixin,
    ResourceListMixin,
    ResourceUpdateMixin,
)

__all__ = [
    "Profiles",
]


class Profiles(
    ResourceBase, ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin
):
    RESOURCE_ID_PREFIX = "pfl_"

    def get_resource_object(self, result):
        return Profile(result, self.client)

    def get(self, profile_id: str, **params):
        if profile_id != "me":
            self.validate_resource_id(profile_id, "profile ID")
        return super().get(profile_id, **params)

    def delete(self, profile_id: str, **params):
        self.validate_resource_id(profile_id, "profile ID")
        return super().delete(profile_id, **params)

    def update(self, profile_id: str, data: dict, **params):
        self.validate_resource_id(profile_id, "profile ID")
        return super().update(profile_id, **params)
