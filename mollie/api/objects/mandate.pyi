from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ..client import Client
    from ..resources.customer_mandates import CustomerMandates
    from ..typing import Final
    from .base import ObjectBase
    from .customer import Customer


class Mandate(ObjectBase):
    @classmethod
    def get_resource_class(cls, client: Client) -> CustomerMandates:
        ...

    STATUS_PENDING: Final[str]
    STATUS_VALID: Final[str]
    STATUS_INVALID: Final[str]

    @property
    def id(self) -> str:
        ...

    @property
    def resource(self) -> str:
        ...

    @property
    def status(self) -> str:
        ...

    @property
    def method(self) -> str:
        ...

    @property
    def details(self) -> dict[str, Any]:
        ...

    @property
    def mandate_reference(self) -> Optional[str]:
        ...

    @property
    def signature_date(self) -> str:
        ...

    @property
    def created_at(self) -> str:
        ...

    def is_pending(self) -> bool:
        ...

    def is_valid(self) -> bool:
        ...

    def is_invalid(self) -> bool:
        ...

    @property
    def customer(self) -> Optional[Customer]:
        ...
