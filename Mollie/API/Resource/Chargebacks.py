from .Base import *


class Chargebacks(Base):
    def getResourceObject(self, result):
        return Chargeback(result)
