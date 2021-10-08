from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ..client import Client
    from .base import ObjectBase


class UnknownObject(ObjectBase):
    @classmethod
    def get_object_name(cls) -> str:
        ...


class ObjectList(ObjectBase):
    def __init__(self, result: dict[str, Any], object_type: Any, client: Optional[Client] = None) -> None:
        ...

    def __len__(self) -> int:
        ...

    def __iter__(self) -> Any:
        ...

    def __next__(self) -> Any:
        ...

    def __getitem__(self, key: str) -> Any:
        ...

    @property
    def count(self) -> int:
        ...

    def has_next(self) -> bool:
        ...

    def has_previous(self) -> bool:
        ...

    def get_next(self) -> "ObjectList":
        ...

    def get_previous(self) -> "ObjectList":
        ...
