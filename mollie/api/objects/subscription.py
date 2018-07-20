from .base import Base


class Subscription(Base):
    STATUS_ACTIVE    = 'active'
    STATUS_PENDING   = 'pending'   # Waiting for a valid mandate.
    STATUS_CANCELLED = 'cancelled'
    STATUS_SUSPENDED = 'suspended' # Active, but mandate became invalid.
    STATUS_COMPLETED = 'completed'

    def is_active(self):
        return self['status'] == self.STATUS_ACTIVE

    def is_pending(self):
        return self['status'] == self.STATUS_PENDING

    def is_cancelled(self):
        return self['status'] == self.STATUS_CANCELLED

    def is_suspended(self):
        return self['status'] == self.STATUS_SUSPENDED

    def is_completed(self):
        return self['status'] == self.STATUS_COMPLETED
