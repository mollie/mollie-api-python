import re
from typing import Optional

from ..error import IdentifierError
from ..objects.settlement import Settlement
from .base import ResourceGetMixin, ResourceListMixin


class Settlements(ResourceGetMixin, ResourceListMixin):
    """Resource handler for the `/settlements` endpoint."""

    RESOURCE_ID_PREFIX = "stl_"

    # According to Mollie, the bank reference is formatted as:
    # - The Mollie customer ID, 4 to 7 digits.
    # - The year and month, 4 digits
    # - The sequence number of the settlement in that month, 2 digits
    # The components are separated by a dot.
    BANK_REFERENCE_REGEX = re.compile(r"^\d{4,7}\.\d{4}\.\d{2}$", re.ASCII)

    def get_resource_object(self, result: dict) -> Settlement:
        return Settlement(result, self.client)  # type: ignore

    @classmethod
    def validate_resource_id(cls, resource_id: str, name: str = "", message: Optional[str] = None) -> None:
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
            try:
                super().validate_resource_id(resource_id)
            except IdentifierError:
                raise IdentifierError(exc_message)

    def get(self, resource_id: str, **params):
        self.validate_resource_id(resource_id)
        return super().get(resource_id, **params)
