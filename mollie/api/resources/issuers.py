from .base import Base
from mollie.api.objects import Issuer


class Issuers(Base):
    def getResourceObject(self, result):
        return Issuer(result)
