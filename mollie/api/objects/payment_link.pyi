from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import Client
    from ..resources.payment_links import PaymentLinks
    from ..typing import Amount
    from .base import ObjectBase


class PaymentLink(ObjectBase):
    @classmethod
    def get_resource_class(cls, client: Client) -> PaymentLinks:
        ...

    @classmethod
    def get_object_name(cls) -> str:
        ...

    @property
    def resource(self) -> str:
        ...

    @property
    def id(self) -> str:
        ...

    @property
    def description(self) -> str:
        ...

    @property
    def mode(self) -> str:
        ...

    @property
    def profile_id(self) -> str:
        ...

    @property
    def amount(self) -> Amount:
        ...

    @property
    def redirect_url(self) -> str:
        ...

    @property
    def webhook_url(self) -> str:
        ...

    @property
    def created_at(self) -> str:
        ...

    @property
    def paid_at(self) -> Optional[str]:
        ...

    @property
    def updated_at(self) -> Optional[str]:
        ...

    @property
    def expires_at(self) -> Optional[str]:
        ...

    @property
    def payment_link(self) -> str:
        ...

    def is_paid(self) -> bool:
        ...

    def has_expiration_date(self) -> bool:
        ...
