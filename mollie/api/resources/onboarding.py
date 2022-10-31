from ..error import IdentifierError
from ..objects.onboarding import Onboarding as OnboardingObject
from .base import ResourceBase, ResourceGetMixin

__all__ = [
    "Onboarding",
]


class Onboarding(ResourceBase, ResourceGetMixin):
    def get_resource_object(self, result):
        return OnboardingObject(result, self.client)

    def get(self, onboarding_id: str, **params):
        if onboarding_id != "me":
            raise IdentifierError(f"Invalid onboarding ID: '{onboarding_id}'. The onboarding ID should be 'me'.")
        return super().get(onboarding_id, **params)

    def create(self, data: dict, **params):
        resource_path = self.get_resource_path()
        path = f"{resource_path}/me"
        result = self.perform_api_call(self.REST_CREATE, path, data, params)
        return self.get_resource_object(result)
