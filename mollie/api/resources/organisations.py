from ..error import IdentifierError
from ..objects.organisation import Organisation
from .base import Base


class Organisations(Base):
    RESOURCE_ID_PREFIX = 'org_'

    def get_resource_object(self, result):
        return Organisation(result, self.client)

    def get(self, organisation_id, **params):
        if not organisation_id or \
                (not organisation_id.startswith(self.RESOURCE_ID_PREFIX)
                 and not organisation_id == 'me'):
            raise IdentifierError(
                "Invalid organisation ID: '{id}'. A organisation ID should start with '{prefix}' "
                "or it should be 'me'.".format(
                    id=organisation_id,
                    prefix=self.RESOURCE_ID_PREFIX)
            )
        return super(Organisations, self).get(organisation_id, **params)
