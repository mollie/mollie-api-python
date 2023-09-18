from .base import ObjectBase


class Invoice(ObjectBase):
    @property
    def id(self):
        return self._get_property("id")

    @property
    def reference(self):
        return self._get_property("reference")

    @property
    def vat_number(self):
        return self._get_property("vatNumber")

    @property
    def status(self):
        return self._get_property("status")

    @property
    def issued_at(self):
        return self._get_property("issuedAt")

    @property
    def paid_at(self):
        return self._get_property("paidAt")

    @property
    def due_at(self):
        return self._get_property("dueAt")

    @property
    def resource(self):
        return self._get_property("resource")

    @property
    def net_amount(self):
        return self._get_property("netAmount")

    @property
    def vat_amount(self):
        return self._get_property("vatAmount")

    @property
    def gross_amount(self):
        return self._get_property("grossAmount")

    @property
    def lines(self):
        return self._get_property("lines") or []

    @property
    def pdf(self):
        return self._get_link("pdf")
