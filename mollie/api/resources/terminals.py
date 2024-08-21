from typing import Any

from ..objects.terminal import Terminal
from .base import ResourceGetMixin, ResourceListMixin

__all__ = [
    "Terminals",
]


class Terminals(ResourceGetMixin, ResourceListMixin):
    """
    Resource handler for the `/terminals` endpoint.

    Retrieve either a single or a list of terminals.
    """

    RESOURCE_ID_PREFIX: str = "term_"
    object_type = Terminal

    def get(self, resource_id: str, **params: Any) -> Terminal:
        """Retrieve a single terminal, by its ID."""
        self.validate_resource_id(resource_id, "terminal ID")
        return super().get(resource_id, **params)
