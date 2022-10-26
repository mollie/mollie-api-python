from ..objects.mandate import Mandate
from .base import ResourceBase, ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin

__all__ = [
    "CustomerMandates",
]


class CustomerMandates(ResourceBase, ResourceCreateMixin, ResourceDeleteMixin, ResourceGetMixin, ResourceListMixin):
    RESOURCE_ID_PREFIX = "mdt_"

    _customer = None

    def __init__(self, client, customer):
        self._customer = customer
        super().__init__(client)

    def get_resource_path(self):
        return f"customers/{self._customer.id}/mandates"

    def get_resource_object(self, result):
        return Mandate(result, self.client)

    def get(self, mandate_id: str, **params):
        self.validate_resource_id(mandate_id, "mandate ID")
        return super().get(mandate_id, **params)

    def delete(self, mandate_id: str, **params):
        self.validate_resource_id(mandate_id, "mandate ID")
        return super().delete(mandate_id, **params)
