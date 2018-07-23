from .base import Base


class Mandate(Base):
    STATUS_PENDING = 'pending'
    STATUS_VALID = 'valid'
    STATUS_INVALID = 'invalid'

    @property
    def id(self):
        return self._get_property('id')

    @property
    def resource(self):
        return self._get_property('resource')

    @property
    def status(self):
        return self._get_property('status')

    @property
    def method(self):
        return self._get_property('method')

    @property
    def details(self):
        return self._get_property('details')

    @property
    def mandate_reference(self):
        return self._get_property('mandateReference')

    @property
    def signature_date(self):
        return self._get_property('signatureDate')

    @property
    def created_at(self):
        return self._get_property('createdAt')

    def is_pending(self):
        return self.status == self.STATUS_PENDING

    def is_valid(self):
        return self.status == self.STATUS_VALID

    def is_invalid(self):
        return self.status == self.STATUS_INVALID
