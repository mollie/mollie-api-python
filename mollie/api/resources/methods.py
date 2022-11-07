from typing import Optional

from ..error import IdentifierError
from ..objects.issuer import Issuer
from ..objects.list import ObjectList
from ..objects.method import Method
from .base import ResourceBase, ResourceGetMixin, ResourceListMixin

__all__ = [
    "Methods",
    "ProfileMethods",
]


class MethodsBase:
    def get_resource_object(self, result: dict) -> Method:
        return Method(result, self.client)  # type: ignore


class Methods(MethodsBase, ResourceGetMixin, ResourceListMixin):
    """Resource handler for the `/methods` endpoint."""

    def all(self, **params) -> ObjectList:
        """List all mollie payment methods, including methods that aren't activated in your profile."""
        resource_path = self.get_resource_path()
        path = f"{resource_path}/all"
        result = self.perform_api_call(self.REST_LIST, path, params=params)
        return ObjectList(result, Method, self.client)


class ProfileMethods(MethodsBase, ResourceBase):
    """Resource handler for the `/profiles/:profile_id:/methods` endpoint."""

    _profile = None

    def __init__(self, client, profile):
        self._profile = profile
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"profiles/{self._profile.id}/methods"  # type: ignore

    @property
    def payment_method_requires_issuer(self):
        """A list of payment methods that requires management of specific issuers."""
        return [
            Method.GIFTCARD,
            Method.VOUCHER,
        ]

    def enable(self, method_id: str, **params):
        """
        Enable payment method for profile.

        For vouchers and giftcards, you need to enable specific issuers using enable_issuer().

        :param method_id: The payment method to enable.
        :type method_id: str
        """
        if method_id in self.payment_method_requires_issuer:
            raise IdentifierError(f"Cannot enable '{method_id}' method, it requires enabling specific issuers.")

        resource_path = self.get_resource_path()
        path = f"{resource_path}/{method_id}"
        result = self.perform_api_call(self.REST_CREATE, path, params=params)
        return self.get_resource_object(result)

    def disable(self, method_id: str, **params):
        """
        Disable payment method for the profile.

        For vouchers and giftcards, you need to enable specific issuers using disable_issuer().

        :param method_id: The payment method to disable.
        :type method_id: str
        """
        if method_id in self.payment_method_requires_issuer:
            raise IdentifierError(f"Cannot disable '{method_id}' method, it requires disabling specific issuers.")

        resource_path = self.get_resource_path()
        path = f"{resource_path}/{method_id}"
        result = self.perform_api_call(self.REST_DELETE, path, params=params)
        return self.get_resource_object(result)

    def list(self, **params):
        """List the payment methods for the profile."""
        params.update({"profileId": self._profile.id})
        # Divert the API call to the general Methods resource
        return Methods(self.client).list(**params)

    def enable_issuer(self, method_id: str, issuer_id: str, data: Optional[dict] = None, **params):
        """
        Enable an issuer for a payment method.

        Vouchers and giftcards need to enable specific issuers, in stead of enabling the payment method in general.

        :param method_id: The payment method, one of: voucher, giftcard.
        :type method_id: str
        :param issuer_id: The issuer to enable.
        :type issuer_id: str
        :param data: Optional payload
        """
        if method_id not in self.payment_method_requires_issuer:
            raise IdentifierError(f"Payment method '{method_id}' does not support issuers.")

        resource_path = self.get_resource_path()
        path = f"{resource_path}/{method_id}/issuers/{issuer_id}"
        result = self.perform_api_call(self.REST_CREATE, path, data, params)
        return Issuer(result, self.client)

    def disable_issuer(self, method_id: str, issuer_id: str, **params):
        """
        Disable an issuer for a payment method.

        Vouchers and giftcards need to disable specific issuers, in stead of disabling the payment method in general.

        :param method_id: The payment method, one of: voucher, giftcard.
        :type method_id: str
        :param issuer_id: The issuer to enable.
        :type issuer_id: str
        """
        if method_id not in self.payment_method_requires_issuer:
            raise IdentifierError(f"Payment method '{method_id}' does not support issuers.")

        resource_path = self.get_resource_path()
        path = f"{resource_path}/{method_id}/issuers/{issuer_id}"
        result = self.perform_api_call(self.REST_DELETE, path, params=params)
        return Issuer(result, self.client)
