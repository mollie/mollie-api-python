from ..error import IdentifierError
from ..objects.profile import Profile
from .base import ResourceBase


class Profiles(ResourceBase):
    RESOURCE_ID_PREFIX = "pfl_"

    def get_resource_object(self, result):
        return Profile(result, self.client)

    def get(self, profile_id, **params):
        if not profile_id or (not profile_id.startswith(self.RESOURCE_ID_PREFIX) and not profile_id == "me"):
            raise IdentifierError(
                f"Invalid profile ID: '{profile_id}'. A profile ID should start with '{self.RESOURCE_ID_PREFIX}' "
                "or it should be 'me'."
            )
        return super().get(profile_id, **params)
