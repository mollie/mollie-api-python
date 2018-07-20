from .base import Base
from mollie.api.objects import Chargeback


class Chargebacks(Base):
    def get_resource_object(self, result):
        return Chargeback(result)
