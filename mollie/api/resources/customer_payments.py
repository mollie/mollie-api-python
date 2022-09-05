import warnings

from ..error import RemovedIn215Warning
from .payments import Payments


class CustomerPayments(Payments):
    # When removing below deprecation warnings, be sure to delete this whole class,
    # and the places where it's being used.

    def with_parent_id(self, *args, **kwargs):
        warnings.warn(
            "Using client.customer_payments is deprecated, use "
            "client.payments.with_parent_id(<customer_id>).list() to retrieve Customer payments.",
            RemovedIn215Warning,
        )
        return super().with_parent_id(*args, **kwargs)

    def on(self, *args, **kwargs):
        warnings.warn(
            "Using client.customer_payments is deprecated, use "
            "client.payments.on(<customer_object>).list() to retrieve Customer payments.",
            RemovedIn215Warning,
        )
        return super().on(*args, **kwargs)
