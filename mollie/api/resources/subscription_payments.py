import warnings

from ..error import RemovedIn215Warning
from .payments import Payments


class SubscriptionPayments(Payments):
    # When removing below deprecation warnings, be sure to delete this whole class,
    # and the places where it's being used.

    customer_id = None
    subscription_id = None

    def get_resource_name(self):
        return f"customers/{self.customer_id}/subscriptions/{self.subscription_id}/payments"

    def with_parent_id(self, customer_id, subscription_id):
        warnings.warn(
            "Using client.subscription_payments is deprecated, use "
            "<subscription object>.payments to retrieve Subscription payments.",
            RemovedIn215Warning,
        )
        self.customer_id = customer_id
        self.subscription_id = subscription_id
        return self

    def on(self, subscription):
        warnings.warn(
            "Using client.subscription_payments is deprecated, use "
            "<subscription object>.payments to retrieve Subscription payments.",
            RemovedIn215Warning,
        )
        # TODO: A request has been filed to mollie to add the customer id to the subscription response.
        return self.with_parent_id(subscription.customer.id, subscription.id)
