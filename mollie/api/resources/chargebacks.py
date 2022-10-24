from ..objects.chargeback import Chargeback
from .base import ResourceBase, ResourceGetMixin, ResourceListMixin


class ChargebacksBase(ResourceBase):
    RESOURCE_ID_PREFIX = "chb_"

    def get_resource_object(self, result):
        return Chargeback(result, self.client)


class Chargebacks(ChargebacksBase, ResourceListMixin):
    pass


class PaymentChargebacks(ChargebacksBase, ResourceGetMixin, ResourceListMixin):
    _payment = None

    def __init__(self, client, payment):
        self._payment = payment
        super().__init__(client)

    def get_resource_path(self):
        return f"payments/{self._payment.id}/chargebacks"

    def get(self, chargeback_id: str, **params):
        self.validate_resource_id(chargeback_id, "chargeback ID")
        return super().get(chargeback_id, **params)
