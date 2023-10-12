from typing import Any

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

    RESOURCE_ID_PREFIX: str = "org_"
    RESULT_CLASS_PATH: str = "mollie.api.objects.client.Client"

    def get(self, resource_id: str, **params: Any) -> Client:
        """Retrieve a single client, linked to your partner account, by its ID."""
        self.validate_resource_id(resource_id, "client ID")
        return super().get(resource_id, **params)
