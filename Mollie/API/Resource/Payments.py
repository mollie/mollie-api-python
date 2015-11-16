from .Base import *
from Mollie.API.Error import *
from Mollie.API.Object import Payment, Refund


class Payments(Base):
    RESOURCE_ID_PREFIX = 'tr_'

    def getResourceObject(self, result):
        return Payment(result)

    def get(self, payment_id):
        if not payment_id or self.RESOURCE_ID_PREFIX not in payment_id:
            raise Error(
                'Invalid payment ID: "%s". A payment ID should start with "%s".' % (payment_id, self.RESOURCE_ID_PREFIX)
            )
        return super(Payments, self).get(payment_id)

    def refund(self, payment):
        return self.client.payment_refunds.on(payment).create()


class Refunds(Base):
    payment_id = None

    def getResourceObject(self, result):
        return Refund(result)

    def getResourceName(self):
        return 'payments/%i/refunds' % self.payment_id

    def on(self, payment):
        self.payment_id = payment['id']
        return self