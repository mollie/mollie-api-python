from .base import Base


class Mandate(Base):
    STATUS_PENDING = 'pending'
    STATUS_VALID   = 'valid'
    STATUS_INVALID = 'invalid'

    def is_pending(self):
        return self['status'] == self.STATUS_PENDING

    def is_valid(self):
        return self['status'] == self.STATUS_VALID

    def is_invalid(self):
        return self['status'] == self.STATUS_INVALID
