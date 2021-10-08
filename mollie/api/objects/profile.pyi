from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import Client
    from ..resources.profiles import Profiles
    from ..typing import Final
    from .base import ObjectBase
    from .list import ObjectList


class Profile(ObjectBase):
    STATUS_UNVERIFIED: Final[str]
    STATUS_VERIFIED: Final[str]
    STATUS_BLOCKED: Final[str]

    @classmethod
    def get_resource_class(cls, client: Client) -> Profiles:
        ...

    @property
    def id(self) -> str:
        ...

    @property
    def resource(self) -> str:
        ...

    @property
    def mode(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def website(self) -> str:
        ...

    @property
    def email(self) -> str:
        ...

    @property
    def phone(self) -> str:
        ...

    @property
    def business_category(self) -> str:
        ...

    @property
    def category_code(self) -> int:
        ...

    @property
    def status(self) -> str:
        ...

    @property
    def review(self) -> Optional[dict[str, str]]:
        ...

    @property
    def created_at(self) -> str:
        ...

    @property
    def chargebacks(self) -> ObjectList:
        ...

    @property
    def methods(self) -> ObjectList:
        ...

    @property
    def payments(self) -> ObjectList:
        ...

    @property
    def refunds(self) -> ObjectList:
        ...

    @property
    def checkout_preview_url(self) -> str:
        ...

    def is_unverified(self) -> bool:
        ...

    def is_verified(self) -> bool:
        ...

    def is_blocked(self) -> bool:
        ...
