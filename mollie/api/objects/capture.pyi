from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import Client
    from ..resources.captures import Captures
    from ..typing import Amount
    from .payment import Payment
    from .settlement import Settlement
    from .shipment import Shipment


class Capture:
    @classmethod
    def get_resource_class(cls, client: Client) -> Captures:
        ...

    @property
    def id(self) -> str:
        ...

    @property
    def mode(self) -> str:
        ...

    @property
    def amount(self) -> Amount:
        ...

    @property
    def settlement_amount(self) -> Optional[Amount]:
        ...

    @property
    def payment_id(self) -> str:
        ...

    @property
    def shipment_id(self) -> Optional[str]:
        ...

    @property
    def settlement_id(self) -> Optional[str]:
        ...

    @property
    def created_at(self) -> str:
        ...

    @property
    def payment(self) -> Payment:
        ...

    @property
    def shipment(self) -> Optional[Shipment]:
        ...

    @property
    def settlement(self) -> Optional[Settlement]:
        ...
