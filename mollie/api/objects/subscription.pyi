from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ..client import Client
    from ..resources.customer_subscriptions import CustomerSubscriptions
    from ..typing import Amount, Final
    from .base import ObjectBase
    from .customer import Customer
    from .list import ObjectList
    from .profile import Profile


class Subscription(ObjectBase):
    @classmethod
    def get_resource_class(cls, client: Client) -> CustomerSubscriptions:
        ...

    STATUS_ACTIVE: Final[str]
    STATUS_PENDING: Final[str]
    STATUS_CANCELED: Final[str]
    STATUS_SUSPENDED: Final[str]
    STATUS_COMPLETED: Final[str]

    @property
    def status(self) -> str:
        ...

    def is_active(self) -> bool:
        ...

    def is_pending(self) -> bool:
        ...

    def is_canceled(self) -> bool:
        ...

    def is_suspended(self) -> bool:
        ...

    def is_completed(self) -> bool:
        ...

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
    def amount(self) -> Amount:
        ...

    @property
    def times(self) -> int:
        ...

    @property
    def times_remaining(self) -> int:
        ...

    @property
    def interval(self) -> str:
        ...

    @property
    def start_date(self) -> str:
        ...

    @property
    def next_payment_date(self) -> Optional[str]:
        ...

    @property
    def description(self) -> str:
        ...

    @property
    def method(self) -> str:
        ...

    @property
    def mandate_id(self) -> Optional[str]:
        ...

    @property
    def canceled_at(self) -> Optional[str]:
        ...

    @property
    def webhook_url(self) -> str:
        ...

    @property
    def metadata(self) -> Optional[dict[Any, Any]]:
        ...

    @property
    def application_fee(self) -> Optional[dict[str, Any]]:
        ...

    @property
    def customer(self) -> Customer:
        ...

    @property
    def profile(self) -> Optional[Profile]:
        ...

    @property
    def payments(self) -> ObjectList:
        ...

    # TODO: Implement this property.
    # Payload from API is missing customerId or a _links['mandate'] field to do this efficiently.
    # @property
    # def mandate(self):
    #     pass
