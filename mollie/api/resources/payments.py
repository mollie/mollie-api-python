from ..error import IdentifierError
from ..objects.payment import Payment
from .base import ResourceAllMethodsMixin, ResourceBase
from .customers import Customers
from .orders import Orders
from .profiles import Profiles
from .settlements import Settlements


class Payments(ResourceBase, ResourceAllMethodsMixin):
    RESOURCE_ID_PREFIX = "tr_"
    parent_id = None

    def get_resource_object(self, result):
        return Payment(result, self.client)

    def get_resource_name(self):
        if not self.parent_id:
            return "payments"

        elif self.parent_id.startswith(Customers.RESOURCE_ID_PREFIX):
            return f"customers/{self.parent_id}/payments"

        elif self.parent_id.startswith(Orders.RESOURCE_ID_PREFIX):
            return f"orders/{self.parent_id}/payments"

        elif self.parent_id.startswith(Profiles.RESOURCE_ID_PREFIX):
            return f"payments?profileId={self.parent_id}"

        elif self.parent_id.startswith(Settlements.RESOURCE_ID_PREFIX):
            return f"settlements/{self.parent_id}/payments"

        else:
            raise IdentifierError(
                "Invalid Parent, the parent of a Payment should be a Customer, an Order, a Profile or a Settlement."
            )

    def get(self, payment_id, **params):
        if not payment_id or not payment_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                f"Invalid payment ID: '{payment_id}'. A payment ID should start with '{self.RESOURCE_ID_PREFIX}'."
            )
        return super().get(payment_id, **params)

    def delete(self, payment_id, data=None):
        """Cancel payment and return the payment object.

        Deleting a payment causes the payment status to change to canceled.
        The updated payment object is returned.
        """
        if not payment_id or not payment_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                f"Invalid payment ID: '{payment_id}'. A payment ID should start with '{self.RESOURCE_ID_PREFIX}'."
            )
        result = super().delete(payment_id, data)
        return self.get_resource_object(result)

    def with_parent_id(self, parent_id):
        self.parent_id = parent_id
        return self

    def on(self, parent):
        return self.with_parent_id(parent.id)
