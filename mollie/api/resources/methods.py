from .base import Base
from mollie.api.objects import Method


class Methods(Base):
    def getResourceObject(self, result):
        return Method(result)
