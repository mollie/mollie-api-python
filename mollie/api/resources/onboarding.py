import warnings
from typing import Any, Dict

from ..error import APIDeprecationWarning, IdentifierError
from ..objects.onboarding import Onboarding as OnboardingObject
from .base import ResourceGetMixin

__all__ = [
    "Onboarding",
]


class Onboarding(ResourceGetMixin):
    """Resource handler for the `/onboarding` endpoint."""

    object_type = OnboardingObject

    def get(self, resource_id: str, **params: Any) -> OnboardingObject:
        if resource_id != "me":
            raise IdentifierError(f"Invalid onboarding ID: '{resource_id}'. The onboarding ID should be 'me'.")
        return super().get(resource_id, **params)

    def create(self, data: Dict[str, Any], **params: Any) -> OnboardingObject:
        warnings.warn(
            "Submission of onboarding data is deprecated, see "
            "https://docs.mollie.com/reference/v2/onboarding-api/submit-onboarding-data",
            APIDeprecationWarning,
        )

        resource_path = self.get_resource_path()
        path = f"{resource_path}/me"
        result = self.perform_api_call(self.REST_CREATE, path, data, params)
        return OnboardingObject(result, self.client)
