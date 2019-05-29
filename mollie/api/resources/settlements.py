from ..error import IdentifierError
from ..objects.settlement import Settlement
from .base import Base


class Settlements(Base):
    RESOURCE_ID_PREFIX = 'stl_'

    def get_resource_object(self, result):
        return Settlement(result, self.client)

    def get(self, settlement_id, **params):
        """Verify the settlement ID and retrieve the settlement from the API."""
        if not settlement_id or (not settlement_id.startswith(
                self.RESOURCE_ID_PREFIX) and settlement_id not in ['next', 'open']):
            raise IdentifierError(
                "Invalid settlement ID: '{id}'. A settlement ID should start with '{prefix}' "
                "or be 'next' or 'open'.".format(
                    id=settlement_id, prefix=self.RESOURCE_ID_PREFIX)
            )
        return super(Settlements, self).get(settlement_id, **params)
