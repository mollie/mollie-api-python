from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:  # pragma: no cover
    from ..client import Client
    from ..resources.orders import Orders
    from ..typing import Amount, Final
    from .base import ObjectBase
    from .list import ObjectList
    from .order_line import OrderLine
    from .payment import Payment
    from .refund import Refund
    from .shipment import Shipment


class Order(ObjectBase):
    def __init__(
        self, data: dict[str, Any], client: Optional[Client] = None, requested_embeds: Optional[list[str]] = None
    ) -> None:
        ...

    def _has_embed(self, embed_name: str) -> bool:
        ...

    @classmethod
    def get_resource_class(cls, client: Client) -> Orders:
        ...

    STATUS_CREATED: Final[str]
    STATUS_PAID: Final[str]
    STATUS_AUTHORIZED: Final[str]
    STATUS_CANCELED: Final[str]
    STATUS_SHIPPING: Final[str]
    STATUS_COMPLETED: Final[str]
    STATUS_EXPIRED: Final[str]

    @property
    def id(self) -> str:
        ...

    @property
    def resource(self) -> str:
        ...

    @property
    def profile_id(self) -> str:
        ...

    @property
    def method(self) -> str:
        ...

    @property
    def mode(self) -> str:
        ...

    @property
    def amount(self) -> Optional[Amount]:
        ...

    @property
    def amount_captured(self) -> Optional[Amount]:
        ...

    @property
    def amount_refunded(self) -> Optional[Amount]:
        ...

    @property
    def status(self) -> str:
        ...

    @property
    def is_cancelable(self) -> bool:
        ...

    @property
    def billing_address(self) -> dict[str, str]:
        ...

    @property
    def consumer_date_of_birth(self) -> Optional[str]:
        ...

    @property
    def order_number(self) -> str:
        ...

    @property
    def shipping_address(self) -> dict[str, str]:
        ...

    @property
    def locale(self) -> str:
        ...

    @property
    def metadata(self) -> Optional[dict[Any, Any]]:
        ...

    @property
    def redirect_url(self) -> Optional[str]:
        ...

    @property
    def webhook_url(self) -> Optional[str]:
        ...

    @property
    def created_at(self) -> str:
        ...

    @property
    def expires_at(self) -> Optional[str]:
        ...

    @property
    def expired_at(self) -> Optional[str]:
        ...

    @property
    def paid_at(self) -> Optional[str]:
        ...

    @property
    def authorized_at(self) -> Optional[str]:
        ...

    @property
    def canceled_at(self) -> Optional[str]:
        ...

    @property
    def completed_at(self) -> Optional[str]:
        ...

    # documented _links

    @property
    def checkout_url(self) -> Optional[str]:
        ...

    # additional methods

    def is_created(self) -> bool:
        ...

    def is_paid(self) -> bool:
        ...

    def is_authorized(self) -> bool:
        ...

    def is_canceled(self) -> bool:
        ...

    def is_shipping(self) -> bool:
        ...

    def is_completed(self) -> bool:
        ...

    def is_expired(self) -> bool:
        ...

    def has_refunds(self) -> bool:
        ...

    def has_shipments(self) -> bool:
        ...

    def create_refund(self, data: Optional[dict[Any, Any]] = None, **params: Optional[dict[str, Any]]) -> Refund:
        ...

    def cancel_lines(self, data: Optional[dict[Any, Any]] = None) -> dict[str, str]:
        ...

    @property
    def refunds(self) -> ObjectList:
        ...

    @property
    def lines(self) -> ObjectList:
        ...

    def update_line(self, resource_id: str, data: dict[str, str]) -> OrderLine:
        ...

    @property
    def shipments(self) -> ObjectList:
        ...

    def create_shipment(self, data: Optional[dict[str, Any]] = None) -> Shipment:
        ...

    def get_shipment(self, resource_id: str) -> Shipment:
        ...

    def update_shipment(self, resource_id: str, data: dict[Any, Any]) -> Shipment:
        ...

    @property
    def payments(self) -> ObjectList:
        ...

    def create_payment(self, data: dict[Any, Any]) -> Payment:
        ...
