from ..error import IdentifierError
from ..objects.client import Client
from .base import ResourceBase


class Clients(ResourceBase):
    """Retrieve a list of Mollie merchants connected to your partner account (only for Mollie partners)."""

    RESOURCE_ID_PREFIX = "org_"

    def get_resource_object(self, result):
        return Client(result, self.client)

    def get(self, client_id, **params):
        """Retrieve a single client, linked to your partner account, by its ID."""
        if not client_id or not client_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                f"Invalid client ID: '{client_id}'. A client ID should start with '{self.RESOURCE_ID_PREFIX}'."
            )
        return super().get(client_id, **params)
