from ..error import IdentifierError
from ..objects.onboarding import Onboarding as OnboardingObject
from .base import Base


class Onboarding(Base):

    def get_resource_object(self, result):
        return OnboardingObject(result, self.client)

    def get(self, onboarding_id, **params):
        if not onboarding_id or not onboarding_id == 'me':
            raise IdentifierError(
                "Invalid refund ID: '{id}'. A refund ID should be 'me'.".format(
                    id=onboarding_id)
            )
        return super(Onboarding, self).get(onboarding_id, **params)
