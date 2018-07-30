from .base import Base
from mollie.api.objects.issuer import Issuer


class Issuers(Base):
    def get_resource_object(self, result):
        return Issuer(result)
