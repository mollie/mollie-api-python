from ..objects.list import ObjectList
from ..objects.payment import Payment
from .base import (
    ResourceBase,
    ResourceCreateMixin,
    ResourceDeleteMixin,
    ResourceGetMixin,
    ResourceListMixin,
    ResourceUpdateMixin,
)

__all__ = [
    "CustomerPayments",
    "OrderPayments",
    "Payments",
]


class PaymentsBase(ResourceBase):
    RESOURCE_ID_PREFIX = "tr_"

    def get_resource_object(self, result):
        from ..objects.payment import Payment

        return Payment(result, self.client)


class Payments(
    PaymentsBase, ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin, ResourceUpdateMixin
):
    def get(self, payment_id: str, **params):
        self.validate_resource_id(payment_id, "payment ID")
        return super().get(payment_id, **params)

    def delete(self, payment_id: str, data=None):
        """Cancel payment and return the payment object.

        Deleting a payment causes the payment status to change to canceled.
        The updated payment object is returned.
        """
        self.validate_resource_id(payment_id, "payment ID")
        result = super().delete(payment_id, data)
        return self.get_resource_object(result)

    def update(self, payment_id: str, data=None):
        self.validate_resource_id(payment_id, "payment ID")
        return super().update(payment_id, data)


class OrderPayments(PaymentsBase, ResourceCreateMixin):
    _order = None

    def __init__(self, client, order):
        self._order = order
        super().__init__(client)

    def get_resource_path(self):
        return f"orders/{self._order.id}/payments"

    def list(self):
        """
        List the payments that might have been embedded in the related order.

        When you receive an EmbedError, you need to embed the payments in the parent order.
        """
        payments = self._order.get_embedded("payments")

        data = {
            "_embedded": {
                "payments": payments,
            },
            "count": len(payments),
        }
        return ObjectList(data, Payment, self.client)


class CustomerPayments(PaymentsBase, ResourceCreateMixin, ResourceListMixin):
    _customer = None

    def __init__(self, client, customer):
        self._customer = customer
        super().__init__(client)

    def get_resource_path(self):
        return f"customers/{self._customer.id}/payments"
