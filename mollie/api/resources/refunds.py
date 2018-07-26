from .base import Base
from mollie.api.error import Error
from mollie.api.objects import Refund


class Refunds(Base):
    RESOURCE_ID_PREFIX = 're_'
    payment_id = None

    def get_resource_object(self, result):
        refund = Refund(result)
        refund._resource = self
        return refund

    def get(self, refund_id, **params):
        if not refund_id or not refund_id.startswith(self.RESOURCE_ID_PREFIX):
            raise Error(
                'Invalid refund ID: "%s". A refund ID should start with "%s".' % (refund_id, self.RESOURCE_ID_PREFIX)
            )
        return super(Refunds, self).get(refund_id)

    def with_parent_id(self, payment_id):
        self.payment_id = payment_id
        return self

    def on(self, payment_id):
        return self.with_parent_id(payment_id)
