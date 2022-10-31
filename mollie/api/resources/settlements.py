import re

from ..error import IdentifierError
from ..objects.settlement import Settlement
from .base import ResourceBase, ResourceGetMixin, ResourceListMixin


class Settlements(ResourceBase, ResourceGetMixin, ResourceListMixin):
    RESOURCE_ID_PREFIX = "stl_"

    # According to Mollie, the bank reference is formatted as:
    # - The Mollie customer ID, 4 to 7 digits.
    # - The year and month, 4 digits
    # - The sequence number of the settlement in that month, 2 digits
    # The components are separated by a dot.
    BANK_REFERENCE_REGEX = re.compile(r"^\d{4,7}\.\d{4}\.\d{2}$", re.ASCII)

    def get_resource_object(self, result):
        return Settlement(result, self.client)

    @classmethod
    def validate_settlement_id(cls, settlement_id: str):
        """
        Validate the reference id to a settlement.

        Valid references for settlements are:
        - The string "next"
        - The string "open"
        - A settlement id, starting with "stl_"
        - A bank reference
        """
        exc_message = (
            f"Invalid settlement ID '{settlement_id}', it should start with '{cls.RESOURCE_ID_PREFIX}', "
            "be 'next' or 'open', or contain a valid bank reference."
        )

        if settlement_id in ["next", "open"]:
            return True

        elif cls.BANK_REFERENCE_REGEX.match(str(settlement_id)):
            return True

        else:
            try:
                cls.validate_resource_id(settlement_id)
            except IdentifierError:
                raise IdentifierError(exc_message)

            return True

    def get(self, settlement_id, **params):
        self.validate_settlement_id(settlement_id)
        return super().get(settlement_id, **params)
