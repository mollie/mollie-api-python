from .Base import Base


class Subscription(Base):
    STATUS_ACTIVE    = 'active'
    STATUS_PENDING   = 'pending'   # Waiting for a valid mandate.
    STATUS_CANCELLED = 'cancelled'
    STATUS_SUSPENDED = 'suspended' # Active, but mandate became invalid.
    STATUS_COMPLETED = 'completed'

    def isActive(self):
        return self['status'] == self.STATUS_ACTIVE

    def isPending(self):
        return self['status'] == self.STATUS_PENDING

    def isCancelled(self):
        return self['status'] == self.STATUS_CANCELLED

    def isSuspended(self):
        return self['status'] == self.STATUS_SUSPENDED

    def isCompleted(self):
        return self['status'] == self.STATUS_COMPLETED
