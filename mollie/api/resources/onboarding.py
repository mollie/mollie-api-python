from ..error import IdentifierError
from ..objects.onboarding import Onboarding as OnboardingObject
from .base import ResourceGetMixin

__all__ = [
    "Onboarding",
]


class Onboarding(ResourceGetMixin):
    """Resource handler for the `/onboarding` endpoint."""

    def get_resource_object(self, result: dict) -> OnboardingObject:
        return OnboardingObject(result, self.client)

    def get(self, resource_id: str, **params):
        if resource_id != "me":
            raise IdentifierError(f"Invalid onboarding ID: '{resource_id}'. The onboarding ID should be 'me'.")
        return super().get(resource_id, **params)

    def create(self, data: dict, **params):
        resource_path = self.get_resource_path()
        path = f"{resource_path}/me"
        result = self.perform_api_call(self.REST_CREATE, path, data, params)
        return self.get_resource_object(result)
