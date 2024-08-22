from typing import Any, Dict, Optional

from ..error import RequestSetupError
from ..objects.client_link import ClientLink
from .base import ResourceCreateMixin

__all__ = [
    "ClientLinks",
]


class ClientLinks(ResourceCreateMixin):
    """Resource handler for the `/client-links` endpoint."""

    RESOURCE_ID_PREFIX: str = "cl_"
    object_type = ClientLink

    def get_resource_path(self) -> str:
        return "client-links"

    def create(self, data: Optional[Dict[str, Any]] = None, idempotency_key: str = "", **params: Any) -> ClientLink:
        if not hasattr(self.client, "_oauth_client"):
            raise RequestSetupError("Creating client links requires OAuth authorization.")
        return super().create(data, idempotency_key, **params)
