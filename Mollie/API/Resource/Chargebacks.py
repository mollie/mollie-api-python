from .Base import Base
from Mollie.API.Object import Chargeback


class Chargebacks(Base):
    def getResourceObject(self, result):
        return Chargeback(result)
