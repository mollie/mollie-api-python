from .base import Base
from mollie.api.objects import Refund


class Refunds(Base):
    def getResourceObject(self, result):
        return Refund(result)
