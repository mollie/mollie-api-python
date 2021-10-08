from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ..client import Client
    from ..resources.refunds import Refunds
    from ..typing import Amount
    from .base import ObjectBase
    from .list import ObjectList
    from .order import Order
    from .payment import Payment


class Refund(ObjectBase):
    @classmethod
    def get_resource_class(cls, client: Client) -> Refunds:
        ...

    # documented properties

    @property
    def resource(self) -> str:
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
    def description(self) -> str:
        ...

    @property
    def status(self) -> str:
        ...

    @property
    def lines(self) -> ObjectList:
        ...

    @property
    def payment_id(self) -> str:
        ...

    @property
    def order_id(self) -> Optional[str]:
        ...

    @property
    def created_at(self) -> str:
        ...

    @property
    def metadata(self) -> Optional[dict[Any, Any]]:
        ...

    # documented _links

    @property
    def payment(self) -> Payment:
        ...

    @property
    def order(self) -> Optional[Order]:
        ...

    # additional methods

    def is_queued(self) -> bool:
        ...

    def is_pending(self) -> bool:
        ...

    def is_processing(self) -> bool:
        ...

    def is_refunded(self) -> bool:
        ...
