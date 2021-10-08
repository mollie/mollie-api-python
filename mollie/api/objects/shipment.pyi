from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .base import ObjectBase
    from .list import ObjectList
    from .order import Order


class Shipment(ObjectBase):
    @property
    def resource(self) -> str:
        ...

    @property
    def id(self) -> str:
        ...

    @property
    def order_id(self) -> str:
        ...

    @property
    def created_at(self) -> str:
        ...

    @property
    def tracking(self) -> Optional[dict[str, str]]:
        ...

    @property
    def tracking_url(self) -> Optional[str]:
        ...

    @property
    def lines(self) -> Optional[ObjectList]:
        ...

    @property
    def order(self) -> Order:
        ...

    def has_tracking(self) -> bool:
        ...

    def has_tracking_url(self) -> bool:
        ...
