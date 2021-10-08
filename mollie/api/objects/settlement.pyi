from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ..client import Client
    from ..resources.settlements import Settlements
    from ..typing import Amount, Final
    from .base import ObjectBase
    from .list import ObjectList


class Settlement(ObjectBase):
    STATUS_OPEN: Final[str]
    STATUS_PENDING: Final[str]
    STATUS_PAIDOUT: Final[str]
    STATUS_FAILED: Final[str]

    @classmethod
    def get_resource_class(cls, client: Client) -> Settlements:
        ...

    @property
    def id(self) -> str:
        ...

    @property
    def reference(self) -> str:
        ...

    @property
    def created_at(self) -> str:
        ...

    @property
    def settled_at(self) -> Optional[str]:
        ...

    @property
    def status(self) -> str:
        ...

    @property
    def amount(self) -> Amount:
        ...

    @property
    def periods(self) -> dict[str, Any]:
        ...

    @property
    def invoice_id(self) -> Optional[str]:
        ...

    def is_open(self) -> bool:
        ...

    def is_pending(self) -> bool:
        ...

    def is_canceled(self) -> bool:
        ...

    def is_failed(self) -> bool:
        ...

    @property
    def payments(self) -> ObjectList:
        ...

    @property
    def refunds(self) -> ObjectList:
        ...

    @property
    def chargebacks(self) -> ObjectList:
        ...

    @property
    def captures(self) -> ObjectList:
        ...

    @property
    def invoice(self) -> str:
        ...
