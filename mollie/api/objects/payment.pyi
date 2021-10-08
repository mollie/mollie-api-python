from typing import TYPE_CHECKING, Any, Optional

from .base import ObjectBase

if TYPE_CHECKING:  # pragma: no cover
    from ..client import Client
    from ..resources.payments import Payments
    from ..typing import Amount
    from .customer import Customer
    from .list import ObjectList
    from .mandate import Mandate
    from .order import Order
    from .settlement import Settlement
    from .subscription import Subscription


class Payment(ObjectBase):
    @classmethod
    def get_resource_class(cls, client: Client) -> Payments:
        ...

    # Documented properties

    @property
    def resource(self) -> str:
        ...

    @property
    def id(self) -> str:
        ...

    @property
    def mode(self) -> str:
        ...

    @property
    def created_at(self) -> str:
        ...

    @property
    def status(self) -> str:
        ...

    @property
    def is_cancelable(self) -> bool:
        ...

    @property
    def authorized_at(self) -> Optional[str]:
        ...

    @property
    def paid_at(self) -> Optional[str]:
        ...

    @property
    def canceled_at(self) -> Optional[str]:
        ...

    @property
    def expires_at(self) -> Optional[str]:
        ...

    @property
    def expired_at(self) -> Optional[str]:
        ...

    @property
    def failed_at(self) -> Optional[str]:
        ...

    @property
    def amount(self) -> dict[str, str]:
        ...

    @property
    def amount_refunded(self) -> Optional[Amount]:
        ...

    @property
    def amount_remaining(self) -> Optional[Amount]:
        ...

    @property
    def amount_captured(self) -> Optional[Amount]:
        ...

    @property
    def amount_chargedback(self) -> Optional[Amount]:
        ...

    @property
    def description(self) -> str:
        ...

    @property
    def redirect_url(self) -> Optional[str]:
        ...

    @property
    def webhook_url(self) -> Optional[str]:
        ...

    @property
    def method(self) -> str:
        ...

    @property
    def metadata(self) -> Optional[dict[Any, Any]]:
        ...

    @property
    def locale(self) -> Optional[str]:
        ...

    @property
    def country_code(self) -> Optional[str]:
        ...

    @property
    def profile_id(self) -> str:
        ...

    @property
    def settlement_amount(self) -> Optional[Amount]:
        ...

    @property
    def settlement_id(self) -> Optional[str]:
        ...

    @property
    def customer_id(self) -> Optional[str]:
        ...

    @property
    def sequence_type(self) -> Optional[str]:
        ...

    @property
    def mandate_id(self) -> Optional[str]:
        ...

    @property
    def subscription_id(self) -> Optional[str]:
        ...

    @property
    def order_id(self) -> Optional[str]:
        ...

    @property
    def application_fee(self) -> Optional[Amount]:
        ...

    @property
    def details(self) -> Optional[dict[Any, Any]]:
        ...

    @property
    def routing(self) -> Optional[list[dict[str, Any]]]:
        ...

    # documented _links

    @property
    def checkout_url(self) -> Optional[str]:
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
    def settlement(self) -> Optional[Settlement]:
        ...

    @property
    def mandate(self) -> Optional[Mandate]:
        ...

    @property
    def subscription(self) -> Optional[Subscription]:
        ...

    @property
    def customer(self) -> Optional[Customer]:
        ...

    @property
    def order(self) -> Optional[Order]:
        ...

    # additional methods

    def is_open(self) -> bool:
        ...

    def is_pending(self) -> bool:
        ...

    def is_canceled(self) -> bool:
        ...

    def is_expired(self) -> bool:
        ...

    def is_failed(self) -> bool:
        ...

    def is_authorized(self) -> bool:
        ...

    def is_paid(self) -> bool:
        ...

    def has_refunds(self) -> bool:
        ...

    def has_chargebacks(self) -> bool:
        ...

    def has_captures(self) -> bool:
        ...

    def has_split_payments(self) -> bool:
        ...

    def can_be_refunded(self) -> bool:
        ...

    def has_sequence_type_first(self) -> bool:
        ...

    def has_sequence_type_recurring(self) -> bool:
        ...
