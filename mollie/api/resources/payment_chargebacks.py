from .chargebacks import Chargebacks


class PaymentChargebacks(Chargebacks):
    payment_id = None

    def get_resource_name(self):
        return 'payments/{id}/chargebacks'.format(id=self.payment_id)

    def with_parent_id(self, payment_id):
        self.payment_id = payment_id
        return self

    def on(self, payment):
        return self.with_parent_id(payment.id)
