import re

from ..error import IdentifierError
from ..objects.settlement import Settlement
from .base import Base


class Settlements(Base):
    RESOURCE_ID_PREFIX = 'stl_'

    # According to Mollie, the bank reference is formatted as:
    # - The Mollie customer ID, 4 to 7 digits.
    # - The year and month, 4 digits
    # - The sequence number of the settlement in that month, 2 digits
    # The components are separated by a dot.
    BANK_REFERENCE_REGEX = re.compile(r'^\d{4,7}\.\d{4}\.\d{2}$', re.ASCII)

    def get_resource_object(self, result):
        return Settlement(result, self.client)

    @classmethod
    def validate_settlement_id(cls, settlement_id):
        if not settlement_id or (
            not settlement_id.startswith(cls.RESOURCE_ID_PREFIX) and
            settlement_id not in ['next', 'open'] and
            not cls.BANK_REFERENCE_REGEX.match(settlement_id)
        ):
            raise IdentifierError(
                "Invalid settlement ID: '{id}'. A settlement ID should start with '{prefix}' "
                ", be 'next' or 'open' or contain a valid bank reference.".format(
                    id=settlement_id, prefix=cls.RESOURCE_ID_PREFIX)
            )

    def get(self, settlement_id, **params):
        self.validate_settlement_id(settlement_id)
        """Verify the settlement ID and retrieve the settlement from the API."""
        return super().get(settlement_id, **params)
