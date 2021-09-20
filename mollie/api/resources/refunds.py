from ..error import IdentifierError
from ..objects.refund import Refund
from .base import ResourceBase


class Refunds(ResourceBase):
    RESOURCE_ID_PREFIX = "re_"

    def get_resource_object(self, result):
        return Refund(result, self.client)

    def get(self, refund_id, **params):
        if not refund_id or not refund_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                f"Invalid refund ID: '{refund_id}'. A refund ID should start with '{self.RESOURCE_ID_PREFIX}'."
            )
        return super().get(refund_id, **params)
