import warnings

from ..error import IdentifierError, RemovedIn215Warning
from ..objects.capture import Capture
from .base import ResourceBase, ResourceGetMixin, ResourceListMixin


class Captures(ResourceBase, ResourceGetMixin, ResourceListMixin):
    RESOURCE_ID_PREFIX = "cpt_"
    parent_id = None

    def get_resource_object(self, result):
        return Capture(result, self.client)

    def get_resource_name(self):
        return f"payments/{self.parent_id}/captures"

    def get(self, capture_id, **params):
        """Verify the capture ID and retrieve the capture from the API."""
        if not capture_id or not capture_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                f"Invalid capture ID: '{capture_id}'. A capture ID should start with '{self.RESOURCE_ID_PREFIX}'."
            )
        return super().get(capture_id, **params)

    def with_parent_id(self, parent_id=None, payment_id=None):
        # When removing this deprecation warning, also remove the default value for 'parent_id'.
        if not parent_id and payment_id:
            warnings.warn("Use parameter 'parent_id' to specify a Parent ID for captures.", RemovedIn215Warning)
            parent_id = payment_id
        self.parent_id = parent_id
        return self

    def on(self, parent=None, payment=None):
        # When removing this deprecation warning, also remove the default value for 'parent_id'.
        if not parent and payment:
            warnings.warn("Use parameter 'parent' to specify a Parent for captures.", RemovedIn215Warning)
            parent = payment
        return self.with_parent_id(parent.id)
