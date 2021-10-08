from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import Client
    from ..resources.chargebacks import Chargebacks
    from ..typing import Amount
    from .base import ObjectBase


class Chargeback(ObjectBase):
    @classmethod
    def get_resource_class(cls, client: Client) -> Chargebacks:
        ...

    @property
    def id(self) -> str:
        ...

    @property
    def amount(self) -> Amount:
        ...

    @property
    def settlement_amount(self) -> Optional[Amount]:
        ...

    @property
    def created_at(self) -> str:
        ...

    @property
    def reversed_at(self) -> Optional[str]:
        ...

    @property
    def payment_id(self) -> str:
        ...
