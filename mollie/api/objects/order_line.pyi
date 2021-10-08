from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ..client import Client
    from ..resources.order_lines import OrderLines
    from ..typing import Amount, Final
    from .base import ObjectBase


class OrderLine(ObjectBase):
    @classmethod
    def get_resource_class(cls, client: Client) -> OrderLines:
        ...

    STATUS_CREATED: Final[str]
    STATUS_AUTHORIZED: Final[str]
    STATUS_PAID: Final[str]
    STATUS_SHIPPING: Final[str]
    STATUS_CANCELED: Final[str]
    STATUS_COMPLETED: Final[str]

    @classmethod
    def get_object_name(cls) -> str:
        ...

    @property
    def id(self) -> str:
        ...

    @property
    def resource(self) -> str:
        ...

    @property
    def order_id(self) -> str:
        ...

    @property
    def type(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def status(self) -> str:
        ...

    @property
    def is_cancelable(self) -> bool:
        ...

    @property
    def quantity(self) -> int:
        ...

    @property
    def quantity_shipped(self) -> int:
        ...

    @property
    def amount_shipped(self) -> Amount:
        ...

    @property
    def quantity_refunded(self) -> int:
        ...

    @property
    def amount_refunded(self) -> Amount:
        ...

    @property
    def quantity_canceled(self) -> int:
        ...

    @property
    def amount_canceled(self) -> Amount:
        ...

    @property
    def shippable_quantity(self) -> int:
        ...

    @property
    def refundable_quantity(self) -> int:
        ...

    @property
    def cancelable_quantity(self) -> int:
        ...

    @property
    def unit_price(self) -> Amount:
        ...

    @property
    def discount_amount(self) -> Amount:
        ...

    @property
    def total_amount(self) -> Amount:
        ...

    @property
    def vat_rate(self) -> str:
        ...

    @property
    def vat_amount(self) -> Amount:
        ...

    @property
    def sku(self) -> Optional[str]:
        ...

    @property
    def image_url(self) -> Optional[str]:
        ...

    @property
    def product_url(self) -> Optional[str]:
        ...

    @property
    def created_at(self) -> str:
        ...

    @property
    def metadata(self) -> Optional[dict[Any, Any]]:
        ...

    def is_created(self) -> bool:
        ...

    def is_authorized(self) -> bool:
        ...

    def is_paid(self) -> bool:
        ...

    def is_shipping(self) -> bool:
        ...

    def is_canceled(self) -> bool:
        ...

    def is_completed(self) -> bool:
        ...
