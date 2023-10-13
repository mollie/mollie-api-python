from .base import ObjectBase


class Onboarding(ObjectBase):
    STATUS_NEEDS_DATA = "needs-data"
    STATUS_IN_REVIEW = "in-review"  # Waiting for a valid mandate.
    STATUS_COMPLETED = "completed"

    @property
    def resource(self):
        return self._get_property("resource")

    @property
    def name(self):
        return self._get_property("name")

    @property
    def signed_up_at(self):
        return self._get_property("signedUpAt")

    @property
    def status(self):
        return self._get_property("status")

    @property
    def can_receive_payments(self):
        return self._get_property("canReceivePayments")

    @property
    def can_receive_settlements(self):
        return self._get_property("canReceiveSettlements")

    def is_needs_data(self):
        return self.status == self.STATUS_NEEDS_DATA

    def is_in_review(self):
        return self.status == self.STATUS_IN_REVIEW

    def is_completed(self):
        return self.status == self.STATUS_COMPLETED

    def get_organization(self):
        """Retrieve the related organization."""
        url = self._get_link("organization")
        if url:
            return self.client.organizations.from_url(url)
