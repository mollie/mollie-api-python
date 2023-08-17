import re
from typing import Any, Pattern

from ..objects.settlement import Settlement
from .base import ResourceGetMixin, ResourceListMixin


class Settlements(ResourceGetMixin, ResourceListMixin):
    """Resource handler for the `/settlements` endpoint."""

    RESOURCE_ID_PREFIX: str = "stl_"
    object_type = Settlement

    # According to Mollie, the bank reference is formatted as:
    # - The Mollie merchant ID, 4 to 8 digits, might grow when the number of merchants increases
    # - The year and month, 4 digits
    # - The sequence number of the settlement in that month, 2 digits
    # The components are separated by a dot.
    BANK_REFERENCE_REGEX: Pattern[str] = re.compile(r"^\d{4,}\.\d{4}\.\d{2}$", re.ASCII)

    @classmethod
    def validate_resource_id(cls, resource_id: str, name: str = "", message: str = "") -> None:
        """
        Validate the reference id to a settlement.

        Valid references for settlements are:
        - The string "next"
        - The string "open"
        - A settlement id, starting with "stl_"
        - A bank reference
        """
        exc_message = (
            f"Invalid settlement ID '{resource_id}', it should start with '{cls.RESOURCE_ID_PREFIX}', "
            "be 'next' or 'open', or contain a valid bank reference."
        )

        if resource_id in ["next", "open"]:
            return

        elif cls.BANK_REFERENCE_REGEX.match(str(resource_id)):
            return

        else:
            super().validate_resource_id(resource_id, message=exc_message)

    def get(self, resource_id: str, **params: Any) -> Settlement:
        self.validate_resource_id(resource_id)
        return super().get(resource_id, **params)
