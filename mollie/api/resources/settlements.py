from ..error import IdentifierError
from ..objects.settlement import Settlement
from .base import Base


class Settlements(Base):
    RESOURCE_ID_PREFIX = 'stl_'

    def get_resource_object(self, result):
        return Settlement(result, self.client)

    @staticmethod
    def validate_settlement_id(RESOURCE_ID_PREFIX, settlement_id):
        if not settlement_id or (not settlement_id.startswith(
                RESOURCE_ID_PREFIX) and settlement_id not in ['next', 'open']):
            raise IdentifierError(
                "Invalid settlement ID: '{id}'. A settlement ID should start with '{prefix}' "
                "or be 'next' or 'open'.".format(
                    id=settlement_id, prefix=RESOURCE_ID_PREFIX)
            )

    def get(self, settlement_id, **params):
        self.validate_settlement_id(self.RESOURCE_ID_PREFIX, settlement_id)
        """Verify the settlement ID and retrieve the settlement from the API."""
        return super(Settlements, self).get(settlement_id, **params)
