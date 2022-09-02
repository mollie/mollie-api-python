from ..error import IdentifierError
from ..objects.chargeback import Chargeback
from .base import ResourceBase, ResourceGetMixin, ResourceListMixin
from .payments import Payments
from .profiles import Profiles
from .settlements import Settlements


class Chargebacks(ResourceBase, ResourceGetMixin, ResourceListMixin):
    RESOURCE_ID_PREFIX = "chb_"
    parent_id = None

    def get_resource_object(self, result):
        return Chargeback(result, self.client)

    def get_resource_name(self):
        if not self.parent_id:
            return "chargebacks"

        elif self.parent_id.startswith(Payments.RESOURCE_ID_PREFIX):
            return f"payments/{self.parent_id}/chargebacks"

        elif self.parent_id.startswith(Settlements.RESOURCE_ID_PREFIX):
            return f"settlements/{self.parent_id}/chargebacks"

        elif self.parent_id.startswith(Profiles.RESOURCE_ID_PREFIX):
            return f"chargebacks?profileId={self.parent_id}"

        else:
            raise IdentifierError("Invalid Parent, the parent of a Chargeback should be a Payment or a Settlement.")

    def get(self, chargeback_id, **params):
        """Verify the chargeback ID and retrieve the chargeback from the API."""
        if not chargeback_id or not chargeback_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                f"Invalid chargeback ID: '{chargeback_id}'. "
                f"A chargeback ID should start with '{self.RESOURCE_ID_PREFIX}'."
            )
        return super().get(chargeback_id, **params)

    def with_parent_id(self, parent_id):
        self.parent_id = parent_id
        return self

    def on(self, parent):
        return self.with_parent_id(parent.id)
