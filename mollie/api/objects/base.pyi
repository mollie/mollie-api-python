from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from ..client import Client


class ObjectBase(Dict[str, Any]):
    def __init__(self, data: dict[str, Any], client: Optional[Client] = None) -> None:
        ...

    def _get_property(self, name: str) -> Any:
        ...

    def _get_link(self, name: str) -> Optional[str]:
        ...

    @classmethod
    def get_object_name(cls) -> str:
        ...

    @classmethod
    def get_resource_class(cls, client: Client) -> Any:
        ...
