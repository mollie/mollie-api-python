from ..error import IdentifierError
from ..objects.capture import Capture
from .base import Base


class Captures(Base):
    RESOURCE_ID_PREFIX = 'cpt_'

    def get_resource_object(self, result):
        return Capture(result, self.client)

    def get_resource_name(self):
        return 'payments/{id}/captures'.format(id=self.payment_id)

    def get(self, capture_id, **params):
        """Verify the capture ID and retrieve the capture from the API."""
        if not capture_id or not capture_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                "Invalid capture ID: '{id}'. A capture ID should start with '{prefix}'.".format(
                    id=capture_id, prefix=self.RESOURCE_ID_PREFIX)
            )
        return super().get(capture_id, **params)

    def with_parent_id(self, payment_id):
        self.payment_id = payment_id
        return self

    def on(self, payment):
        return self.with_parent_id(payment.id)
