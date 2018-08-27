from ..error import IdentifierError
from ..objects.refund import Refund
from .base import Base


class Refunds(Base):
    RESOURCE_ID_PREFIX = 're_'

    def get_resource_object(self, result):
        return Refund(result, self)

    def get(self, refund_id, **params):
        if not refund_id or not refund_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                "Invalid refund ID: '{id}'. A refund ID should start with '{prefix}'.".format(
                    id=refund_id, prefix=self.RESOURCE_ID_PREFIX)
            )
        return super(Refunds, self).get(refund_id, **params)
