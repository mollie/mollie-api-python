from .Base import *
from Mollie.API.Object import Issuer


class Issuers(Base):
    def getResourceObject(self, result):
        return Issuer(result)