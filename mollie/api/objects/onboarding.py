from .base import Base


class Onboarding(Base):
    @classmethod
    def get_resource_class(cls, client):
        from ..resources.refunds import Refunds
        return Refunds(client)

    @property
    def resource(self):
        return self._get_property('resource')

    @property
    def name(self):
        return self._get_property('name')

    @property
    def signed_up_at(self):
        return self._get_property('signedUpAt')

    @property
    def status(self):
        return self._get_property('status')

    @property
    def can_receive_payments(self):
        return self._get_property('canReceivePayments')

    @property
    def can_receive_settlements(self):
        return self._get_property('canReceiveSettlements')
