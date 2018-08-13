from ..error import IdentifierError
from ..objects.refund import Refund
from .base import Base


class Refunds(Base):
    RESOURCE_ID_PREFIX = 're_'
    payment_id = None

    def get_resource_object(self, result):
        refund = Refund(result)
        refund._resource = self
        return refund

    def get(self, refund_id, **params):
        if not refund_id or not refund_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                'Invalid refund ID: "%s". A refund ID should start with "%s".' % (refund_id, self.RESOURCE_ID_PREFIX)
            )
        return super(Refunds, self).get(refund_id, **params)

    def with_parent_id(self, payment_id):
        self.payment_id = payment_id
        return self

    def on(self, payment_id):
        return self.with_parent_id(payment_id)
