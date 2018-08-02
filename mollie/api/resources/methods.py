from ..objects.method import Method
from .base import Base


class Methods(Base):
    def get_resource_object(self, result):
        return Method(result)
