from .Base import *
from Mollie.API.Error import *
from Mollie.API.Object import Payment, Refund


class Payments(Base):
    RESOURCE_ID_PREFIX = 'tr_'

    def getResourceObject(self, result):
        return Payment(result)

    def get(self, payment_id):
        if not payment_id or not payment_id.startswith(self.RESOURCE_ID_PREFIX):
            raise Error(
                'Invalid payment ID: "%s". A payment ID should start with "%s".' % (payment_id, self.RESOURCE_ID_PREFIX)
            )
        return super(Payments, self).get(payment_id)

    def refunds(self, payment):
        return self.client.payment_refunds.on(payment)

    def refund(self, payment, data=None):
        return self.refunds(payment).create(data)

class Refunds(Base):
    payment_id = None

    def getResourceObject(self, result):
        return Refund(result)

    def getResourceName(self):
        return 'payments/%s/refunds' % self.payment_id

    def withParentId(self, payment_id):
        self.payment_id = payment_id
        return self

    def on(self, payment):
        return self.withParentId(payment['id'])
