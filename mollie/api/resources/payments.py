from .base import Base
from mollie.api.error import Error
from mollie.api.objects import Payment


class Payments(Base):
    RESOURCE_ID_PREFIX = 'tr_'

    def get_resource_object(self, result):
        return Payment(result)

    def get(self, payment_id, **params):
        if not payment_id or not payment_id.startswith(self.RESOURCE_ID_PREFIX):
            raise Error(
                'Invalid payment ID: "%s". A payment ID should start with "%s".' % (payment_id, self.RESOURCE_ID_PREFIX)
            )
        return super(Payments, self).get(payment_id)

    def refunds(self, payment):
        return self.client.payment_refunds.on(payment)

    def chargebacks(self, payment):
        return self.client.payment_chargebacks.on(payment)

    def refund(self, payment, data=None, **params):
        return self.refunds(payment).create(data, **params)
