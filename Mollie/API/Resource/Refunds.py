from .Base import *


class Refunds(Base):
    def getResourceObject(self, result):
        return Refund(result)
