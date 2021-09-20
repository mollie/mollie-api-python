from ..error import IdentifierError
from ..objects.organization import Organization
from .base import ResourceBase


class Organizations(ResourceBase):
    RESOURCE_ID_PREFIX = "org_"

    def get_resource_object(self, result):
        return Organization(result, self.client)

    def get(self, organization_id, **params):
        if not organization_id or (
            not organization_id.startswith(self.RESOURCE_ID_PREFIX) and not organization_id == "me"
        ):
            raise IdentifierError(
                f"Invalid organization ID: '{organization_id}'. A organization ID should start "
                f"with '{self.RESOURCE_ID_PREFIX}' or it should be 'me'."
            )
        return super().get(organization_id, **params)
