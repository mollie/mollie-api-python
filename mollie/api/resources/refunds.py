from .base import Base
from mollie.api.objects import Refund


class Refunds(Base):
    def get_resource_object(self, result):
        refund = Refund(result)
        refund._resource = self
        return refund
