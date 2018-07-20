from .base import Base
from mollie.api.objects import Chargeback


class Chargebacks(Base):
    def getResourceObject(self, result):
        return Chargeback(result)
