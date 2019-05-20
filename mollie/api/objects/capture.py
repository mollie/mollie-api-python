from .base import Base


class Capture(Base):
    @classmethod
    def get_resource_class(cls, client):
        from ..resources.captures import Captures
        return Captures(client)

    @property
    def id(self):
        return self._get_property('id')

    @property
    def mode(self):
        return self._get_property('mode')

    @property
    def amount(self):
        return self._get_property('amount')

    @property
    def settlementAmount(self):
        return self._get_property('settlementAmount')

    @property
    def paymentId(self):
        return self._get_property('paymentId')

    @property
    def shipmentId(self):
        return self._get_property('shipmentId')

    @property
    def settlementId(self):
        return self._get_property('settlementId')

    @property
    def createdAt(self):
        return self._get_property('createdAt')
