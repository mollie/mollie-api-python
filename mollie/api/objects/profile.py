import warnings

from ..error import APIDeprecationWarning
from .base import ObjectBase


class Profile(ObjectBase):
    STATUS_UNVERIFIED = "unverified"
    STATUS_VERIFIED = "verified"
    STATUS_BLOCKED = "blocked"

    @classmethod
    def get_resource_class(cls, client):
        from ..resources.profiles import Profiles

        return Profiles(client)

    @property
    def id(self):
        return self._get_property("id")

    @property
    def resource(self):
        return self._get_property("resource")

    @property
    def mode(self):
        return self._get_property("mode")

    @property
    def name(self):
        return self._get_property("name")

    @property
    def website(self):
        return self._get_property("website")

    @property
    def email(self):
        return self._get_property("email")

    @property
    def phone(self):
        return self._get_property("phone")

    @property
    def business_category(self):
        return self._get_property("businessCategory")

    @property
    def category_code(self):
        warnings.warn(
            "Using categoryCode is deprecated, see https://docs.mollie.com/reference/v2/profiles-api/get-profile",
            APIDeprecationWarning,
        )
        return self._get_property("categoryCode")

    @property
    def status(self):
        return self._get_property("status")

    @property
    def review(self):
        return self._get_property("review")

    @property
    def created_at(self):
        return self._get_property("createdAt")

    @property
    def chargebacks(self):
        return self.client.chargebacks.on(self).list()

    @property
    def methods(self):
        return self.client.profile_methods.on(self).list()

    @property
    def payments(self):
        return self.client.payments.on(self).list()

    @property
    def refunds(self):
        return self.client.profile_refunds.on(self).list()

    @property
    def checkout_preview_url(self):
        return self._get_link("checkoutPreviewUrl")

    # additional methods

    def is_unverified(self):
        return self._get_property("status") == self.STATUS_UNVERIFIED

    def is_verified(self):
        return self._get_property("status") == self.STATUS_VERIFIED

    def is_blocked(self):
        return self._get_property("status") == self.STATUS_BLOCKED
