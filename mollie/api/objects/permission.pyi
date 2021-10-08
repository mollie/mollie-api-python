from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import Client
    from ..resources.permissions import Permissions
    from .base import ObjectBase


class Permission(ObjectBase):
    @classmethod
    def get_resource_class(cls, client: Client) -> Permissions:
        ...

    @property
    def id(self) -> str:
        ...

    @property
    def resource(self) -> str:
        ...

    @property
    def description(self) -> str:
        ...

    @property
    def granted(self) -> bool:
        ...
