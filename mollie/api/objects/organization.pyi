from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import Client
    from ..resources.organizations import Organizations
    from .base import ObjectBase


class Organization(ObjectBase):
    @classmethod
    def get_resource_class(cls, client: Client) -> Organizations:
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
    def address(self) -> dict[str, str]:
        ...

    @property
    def registration_number(self) -> str:
        ...

    @property
    def vat_number(self) -> Optional[str]:
        ...

    @property
    def vat_regulation(self) -> Optional[str]:
        ...

    @property
    def dashboard(self) -> str:
        ...
