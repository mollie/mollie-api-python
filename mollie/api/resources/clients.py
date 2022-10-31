from ..objects.client import Client
from .base import ResourceBase, ResourceGetMixin, ResourceListMixin

__all__ = [
    "Clients",
]


class Clients(ResourceBase, ResourceListMixin, ResourceGetMixin):
    """Retrieve a list of Mollie merchants connected to your partner account (only for Mollie partners)."""

    RESOURCE_ID_PREFIX = "org_"

    def get_resource_object(self, result):
        return Client(result, self.client)

    def get(self, client_id: str, **params):
        """Retrieve a single client, linked to your partner account, by its ID."""
        self.validate_resource_id(client_id, "client ID")
        return super().get(client_id, **params)
