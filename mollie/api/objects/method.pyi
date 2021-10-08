from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import Client
    from ..resources.methods import Methods
    from ..typing import Amount, Final
    from .base import ObjectBase
    from .list import ObjectList


class Method(ObjectBase):
    @classmethod
    def get_resource_class(cls, client: Client) -> Methods:
        ...

    BANCONTACT: Final[str]
    BANKTRANSFER: Final[str]
    BELFIUS: Final[str]
    CREDITCARD: Final[str]
    DIRECTDEBIT: Final[str]
    EPS: Final[str]
    GIFTCARD: Final[str]
    GIROPAY: Final[str]
    IDEAL: Final[str]
    KBC: Final[str]
    KLARNAPAYLATER: Final[str]
    KLARNAPAYNOW: Final[str]
    KLARNASLICEIT: Final[str]
    MEALVOUCHER: Final[str]
    MISTERCASH: Final[str]
    MYBANK: Final[str]
    PAYPAL: Final[str]
    PAYSAFECARD: Final[str]
    PODIUMCADEAUKAART: Final[str]
    PRZELEWY24: Final[str]
    SOFORT: Final[str]

    @property
    def description(self) -> str:
        ...

    @property
    def id(self) -> str:
        ...

    @property
    def minimum_amount(self) -> Amount:
        ...

    @property
    def maximum_amount(self) -> Amount:
        ...

    @property
    def pricing(self) -> list[dict[str, Any]]:
        ...

    @property
    def image_svg(self) -> str:
        ...

    @property
    def image_size1x(self) -> str:
        ...

    @property
    def image_size2x(self) -> str:
        ...

    @property
    def issuers(self) -> ObjectList:
        ...
