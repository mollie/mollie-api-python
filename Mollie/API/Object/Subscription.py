from .Base import *


class Subscription(Base):
    STATUS_ACTIVE    = 'active'
    STATUS_PENDING   = 'pending'   # Waiting for a valid mandate.
    STATUS_CANCELLED = 'cancelled'
    STATUS_SUSPENDED = 'suspended' # Active, but mandate became invalid.
    STATUS_COMPLETED = 'completed'
