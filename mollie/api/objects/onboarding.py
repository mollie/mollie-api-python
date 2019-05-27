from .base import Base


class Onboarding(Base):
    @classmethod
    def get_resource_class(cls, client):
        from ..resources.onboarding import Onboarding as OnboardingResource
        return OnboardingResource(client)

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

    @property
    def organisation(self):
        """Retrieve organisation for an onboarding."""
        from .organisation import Organisation
        url = self._get_link('organization')

        if url:
            resp = self.client.organisations.perform_api_call(self.client.organisations.REST_READ, url)
            return Organisation(resp)
