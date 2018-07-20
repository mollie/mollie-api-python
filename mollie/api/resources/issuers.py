from .base import Base
from mollie.api.objects import Issuer


class Issuers(Base):
    def get_resource_object(self, result):
        return Issuer(result)
