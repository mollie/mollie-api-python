from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base import ObjectBase


class Issuer(ObjectBase):
    @property
    def resource(self) -> str:
        ...

    @property
    def id(self) -> str:
        ...

    @property
    def name(self) -> str:
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
