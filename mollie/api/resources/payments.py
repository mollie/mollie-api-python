from .base import (
    ResourceBase,
    ResourceCreateMixin,
    ResourceDeleteMixin,
    ResourceGetMixin,
    ResourceListMixin,
    ResourceUpdateMixin,
)


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
