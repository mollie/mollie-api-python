from Mollie.API.Resource import Chargebacks


class PaymentChargebacks(Chargebacks):
    payment_id = None

    def getResourceName(self):
        return 'payments/%s/chargebacks' % self.payment_id

    def withParentId(self, payment_id):
        self.payment_id = payment_id
        return self

    def on(self, payment):
        return self.withParentId(payment['id'])
