from ..error import IdentifierError
from ..objects.organization import Organization
from .base import Base


class Organizations(Base):
    RESOURCE_ID_PREFIX = 'org_'

    def get_resource_object(self, result):
        return Organization(result, self.client)

    def get(self, organization_id, **params):
        if not organization_id or \
                (not organization_id.startswith(self.RESOURCE_ID_PREFIX)
                 and not organization_id == 'me'):
            raise IdentifierError(
                "Invalid organization ID: '{id}'. A organization ID should start with '{prefix}' "
                "or it should be 'me'.".format(
                    id=organization_id,
                    prefix=self.RESOURCE_ID_PREFIX)
            )
        return super().get(organization_id, **params)
