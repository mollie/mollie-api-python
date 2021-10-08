from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ..client import Client
    from ..resources.customers import Customers
    from .base import ObjectBase
    from .list import ObjectList


class Customer(ObjectBase):
    @classmethod
    def get_resource_class(cls, client: Client) -> Customers:
        ...

    @property
    def id(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def email(self) -> str:
        ...

    @property
    def locale(self) -> str:
        ...

    @property
    def metadata(self) -> Optional[dict[Any, Any]]:
        ...

    @property
    def mode(self) -> str:
        ...

    @property
    def resource(self) -> str:
        ...

    @property
    def created_at(self) -> str:
        ...

    @property
    def subscriptions(self) -> ObjectList:
        ...

    @property
    def mandates(self) -> ObjectList:
        ...

    @property
    def payments(self) -> ObjectList:
        ...
