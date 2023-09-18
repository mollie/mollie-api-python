import warnings

from ..error import APIDeprecationWarning
from .base import ObjectBase


class Profile(ObjectBase):
    STATUS_UNVERIFIED = "unverified"
    STATUS_VERIFIED = "verified"
    STATUS_BLOCKED = "blocked"

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
        from ..resources import ProfileChargebacks

        return ProfileChargebacks(self.client, self)

    @property
    def methods(self):
        from ..resources import ProfileMethods

        return ProfileMethods(self.client, self)

    @property
    def payments(self):
        from ..resources import ProfilePayments

        return ProfilePayments(self.client, self)

    @property
    def refunds(self):
        from ..resources import ProfileRefunds

        return ProfileRefunds(self.client, self)

    @property
    def checkout_preview_url(self):
        return self._get_link("checkoutPreviewUrl")

    # additional methods

    def is_unverified(self):
        return self.status == self.STATUS_UNVERIFIED

    def is_verified(self):
        return self.status == self.STATUS_VERIFIED

    def is_blocked(self):
        return self.status == self.STATUS_BLOCKED
