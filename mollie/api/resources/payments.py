from .base import Base
from mollie.api.error import Error
from mollie.api.objects.payment import Payment


class Payments(Base):
    RESOURCE_ID_PREFIX = 'tr_'

    def get_resource_object(self, result):
        payment = Payment(result)
        payment._resource = self
        return payment

    def get(self, payment_id, **params):
        if not payment_id or not payment_id.startswith(self.RESOURCE_ID_PREFIX):
            raise Error(
                'Invalid payment ID: "%s". A payment ID should start with "%s".' % (
                    payment_id, self.RESOURCE_ID_PREFIX)
            )
        return super(Payments, self).get(payment_id)

    def delete(self, resource_id):
        """Cancel payment and return the payment object.

        Deleting a payment causes the payment status to change to canceled.
        The updated payment object is returned.
        """
        if not resource_id or not resource_id.startswith(self.RESOURCE_ID_PREFIX):
            raise Error(
                'Invalid payment ID: "%s". A payment ID should start with "%s".' % (
                    resource_id, self.RESOURCE_ID_PREFIX))
        result = super(Payments, self).delete(resource_id)
        return self.get_resource_object(result)
