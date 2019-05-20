from ..error import IdentifierError
from ..objects.capture import Capture
from .base import Base


class Captures(Base):
    RESOURCE_ID_PREFIX = 'cap_'

    def get_resource_object(self, result):
        return Capture(result)

    def get_resource_name(self):
        return 'payments/{id}/captures'.format(id=self.payment_id)

    def get(self, capture_id, **params):
        """Verify the chargeback ID and retrieve the chargeback from the API."""
        if not capture_id or not capture_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                "Invalid chargeback ID: '{id}'. A chargeback ID should start with '{prefix}'.".format(
                    id=capture_id, prefix=self.RESOURCE_ID_PREFIX)
            )
        return super(Captures, self).get(capture_id, **params)

    def with_parent_id(self, payment_id):
        self.payment_id = payment_id
        return self
