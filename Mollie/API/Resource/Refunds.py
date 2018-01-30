from .Base import Base
from Mollie.API.Object import Refund


class Refunds(Base):
    def getResourceObject(self, result):
        return Refund(result)
