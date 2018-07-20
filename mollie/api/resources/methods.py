from .base import Base
from mollie.api.objects import Method


class Methods(Base):
    def get_resource_object(self, result):
        return Method(result)
