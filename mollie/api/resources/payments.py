from ..error import IdentifierError
from ..objects.payment import Payment
from .base import Base


class Payments(Base):
    RESOURCE_ID_PREFIX = 'tr_'

    def get_resource_object(self, result):
        return Payment(result, self)

    def get(self, payment_id, **params):
        if not payment_id or not payment_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                'Invalid payment ID: "%s". A payment ID should start with "%s".' % (
                    payment_id, self.RESOURCE_ID_PREFIX)
            )
        return super(Payments, self).get(payment_id, **params)

    def delete(self, resource_id):
        """Cancel payment and return the payment object.

        Deleting a payment causes the payment status to change to canceled.
        The updated payment object is returned.
        """
        if not resource_id or not resource_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                'Invalid payment ID: "%s". A payment ID should start with "%s".' % (
                    resource_id, self.RESOURCE_ID_PREFIX))
        result = super(Payments, self).delete(resource_id)
        return self.get_resource_object(result)
