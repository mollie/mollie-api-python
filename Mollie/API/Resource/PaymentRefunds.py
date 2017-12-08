from Mollie.API.Resource import Refunds


class PaymentRefunds(Refunds):
    payment_id = None

    def getResourceName(self):
        return 'payments/%s/refunds' % self.payment_id

    def withParentId(self, payment_id):
        self.payment_id = payment_id
        return self

    def on(self, payment):
        return self.withParentId(payment['id'])
