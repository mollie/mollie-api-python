from .Base import Base


class Mandate(Base):
    STATUS_PENDING = 'pending'
    STATUS_VALID   = 'valid'
    STATUS_INVALID = 'invalid'

    def isPending(self):
        return self['status'] == self.STATUS_PENDING

    def isValid(self):
        return self['status'] == self.STATUS_VALID

    def isInvalid(self):
        return self['status'] == self.STATUS_INVALID
