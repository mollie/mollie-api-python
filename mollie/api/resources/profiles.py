from ..error import IdentifierError
from ..objects.profile import Profile
from .base import Base


class Profiles(Base):
    RESOURCE_ID_PREFIX = 'pfl_'

    def get_resource_object(self, result):
        return Profile(result, self.client)

    def get(self, profile_id, **params):
        if not profile_id or \
                (not profile_id.startswith(self.RESOURCE_ID_PREFIX)
                 and not profile_id == 'me'):
            raise IdentifierError(
                "Invalid profile ID: '{id}'. A profile ID should start with '{prefix}' "
                "or it should be 'me'.".format(
                    id=profile_id,
                    prefix=self.RESOURCE_ID_PREFIX)
            )
        return super().get(profile_id, **params)
