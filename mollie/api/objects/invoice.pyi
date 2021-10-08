from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ..client import Client
    from ..resources.invoices import Invoices
    from ..typing import Amount
    from .base import ObjectBase


class Invoice(ObjectBase):
    @classmethod
    def get_resource_class(cls, client: Client) -> Invoices:
        ...

    @property
    def id(self) -> str:
        ...

    @property
    def reference(self) -> str:
        ...

    @property
    def vat_number(self) -> str:
        ...

    @property
    def status(self) -> str:
        ...

    @property
    def issued_at(self) -> str:
        ...

    # TODO add paid_at attribute

    @property
    def due_at(self) -> Optional[str]:
        ...

    @property
    def resource(self) -> str:
        ...

    @property
    def net_amount(self) -> Amount:
        ...

    @property
    def vat_amount(self) -> Optional[Amount]:
        ...

    @property
    def gross_amount(self) -> Amount:
        ...

    @property
    def lines(self) -> list[dict[str, Any]]:
        ...

    @property
    def pdf(self) -> str:
        ...
