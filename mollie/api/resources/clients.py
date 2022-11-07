from ..objects.client import Client
from .base import ResourceGetMixin, ResourceListMixin

__all__ = [
    "Clients",
]


class Clients(ResourceListMixin, ResourceGetMixin):
    """
    Resource handler for the `/clients` endpoint.

    Retrieve a list of Mollie merchants connected to your partner account (only for Mollie partners).
    """

    RESOURCE_ID_PREFIX = "org_"

    def get_resource_object(self, result: dict) -> Client:
        return Client(result, self.client)

    def get(self, resource_id: str, **params):
        """Retrieve a single client, linked to your partner account, by its ID."""
        self.validate_resource_id(resource_id, "client ID")
        return super().get(resource_id, **params)
