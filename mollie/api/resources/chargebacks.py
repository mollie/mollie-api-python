from .base import Base
from mollie.api.error import IdentifierValidationError
from mollie.api.objects import Chargeback


class Chargebacks(Base):
    RESOURCE_ID_PREFIX = 'chb_'

    def get_resource_object(self, result):
        return Chargeback(result)

    def get(self, chargeback_id, **params):
        """Verify the chargeback ID and retrieve the chargeback from the API."""
        if not chargeback_id or not chargeback_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierValidationError(
                'Invalid chargeback ID: "%s". A chargeback ID should start with "%s".' % (
                    chargeback_id, self.RESOURCE_ID_PREFIX)
            )
        return super(Chargebacks, self).get(chargeback_id)
