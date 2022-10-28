from ..error import IdentifierError
from ..objects.list import ObjectList
from ..objects.method import Method
from .base import ResourceBase, ResourceGetMixin, ResourceListMixin

__all__ = [
    "Methods",
    "ProfileMethods",
]


class MethodsBase(ResourceBase):
    def get_resource_object(self, result):
        return Method(result, self.client)


class Methods(MethodsBase, ResourceGetMixin, ResourceListMixin):
    def all(self, **params):
        """List all mollie payment methods, including methods that aren't activated in your profile."""
        resource_path = self.get_resource_path()
        path = f"{resource_path}/all"
        result = self.perform_api_call(self.REST_LIST, path, params=params)
        return ObjectList(result, Method, self.client)


class ProfileMethods(MethodsBase, ResourceListMixin):
    _profile = None

    def __init__(self, client, profile):
        self._profile = profile
        super().__init__(client)

    def get_resource_path(self):
        return f"profiles/{self._profile.id}/methods"

    def enable(self, method_id: str, issuer_id: str = None, **params):
        """
        Enable payment method for profile.

        For vouchers and giftcards, you need to provide the relevant issuer_id.
        """
        if method_id in [Method.VOUCHER, Method.GIFTCARD]:
            if not issuer_id:
                raise IdentifierError(f"Cannot enable '{method_id}' method, no issuer specified.")
            else:
                raise NotImplementedError("TODO")

        resource_path = self.get_resource_path()
        path = f"{resource_path}/{method_id}"
        result = self.perform_api_call(self.REST_CREATE, path, params=params)
        return self.get_resource_object(result)

    def disable(self, method_id: str, issuer_id: str = None, **params):
        """
        Disable payment method for the profile.

        For vouchers and giftcards, you need to provide the relevant issuer_id.
        """
        if method_id in [Method.VOUCHER, Method.GIFTCARD]:
            if not issuer_id:
                raise IdentifierError(f"Cannot disable '{method_id}' method, no issuer specified.")
            else:
                raise NotImplementedError("TODO")

        resource_path = self.get_resource_path()
        path = f"{resource_path}/{method_id}"
        result = self.perform_api_call(self.REST_DELETE, path, params=params)
        return self.get_resource_object(result)

    def list(self, **params):
        """List the payment methods for the profile."""
        params.update({"profileId": self._profile.id})
        # Divert the API call to the general Methods resource
        return Methods(self.client).list(**params)
