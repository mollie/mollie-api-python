from ..error import IdentifierError
from ..objects.chargeback import Chargeback
from .base import ResourceBase


class Chargebacks(ResourceBase):
    RESOURCE_ID_PREFIX = "chb_"

    def get_resource_object(self, result):
        return Chargeback(result)

    def get(self, chargeback_id, **params):
        """Verify the chargeback ID and retrieve the chargeback from the API."""
        if not chargeback_id or not chargeback_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                f"Invalid chargeback ID: '{chargeback_id}'. "
                f"A chargeback ID should start with '{self.RESOURCE_ID_PREFIX}'."
            )
        return super().get(chargeback_id, **params)
