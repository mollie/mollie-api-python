import warnings

from ..error import RemovedIn215Warning
from .subscriptions import Subscriptions


class CustomerSubscriptions(Subscriptions):
    # When removing below deprecation warnings, be sure to delete this whole class,
    # and the places where it's being used.

    def with_parent_id(self, customer_id):
        warnings.warn(
            "Using client.customer_subscriptions is deprecated, use "
            "client.payments.with_parent_id(<customer_id>).list() to retrieve Customer payments.",
            RemovedIn215Warning,
        )
        return super().with_parent_id(customer_id)

    def on(self, customer):
        warnings.warn(
            "Using client.customer_subscriptions is deprecated, use "
            "client.payments.on(<customer_object>).list() to retrieve Customer payments.",
            RemovedIn215Warning,
        )
        return super().on(customer)
