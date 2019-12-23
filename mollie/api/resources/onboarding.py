from ..error import IdentifierError
from ..objects.onboarding import Onboarding as OnboardingObject
from .base import Base


class Onboarding(Base):

    def get_resource_object(self, result):
        return OnboardingObject(result, self.client)

    def get(self, onboarding_id, **params):
        if not onboarding_id or not onboarding_id == 'me':
            raise IdentifierError(
                "Invalid onboarding ID: '{id}'. A onboarding ID should be 'me'.".format(
                    id=onboarding_id)
            )
        return super().get(onboarding_id, **params)

    def create(self, resource_id, data=None, **params):
        path = self.get_resource_name() + '/' + str(resource_id)
        result = self.perform_api_call(self.REST_CREATE, path, data, params)
        return self.get_resource_object(result)
