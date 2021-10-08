from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import Client
    from ..resources.onboarding import Onboarding as OnboardingResource
    from ..typing import Final
    from .base import ObjectBase
    from .organization import Organization


class Onboarding(ObjectBase):
    @classmethod
    def get_resource_class(cls, client: Client) -> OnboardingResource:
        ...

    STATUS_NEEDS_DATA: Final[str]
    STATUS_IN_REVIEW: Final[str]
    STATUS_COMPLETED: Final[str]

    @property
    def resource(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def signed_up_at(self) -> str:
        ...

    @property
    def status(self) -> str:
        ...

    @property
    def can_receive_payments(self) -> bool:
        ...

    @property
    def can_receive_settlements(self) -> bool:
        ...

    @property
    def organization(self) -> Optional[Organization]:
        ...

    def is_needs_data(self) -> bool:
        ...

    def is_in_review(self) -> bool:
        ...

    def is_completed(self) -> bool:
        ...
