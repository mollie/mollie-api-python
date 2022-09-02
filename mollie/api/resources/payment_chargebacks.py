import warnings

from ..error import RemovedIn215Warning
from .chargebacks import Chargebacks


class PaymentChargebacks(Chargebacks):
    # When removing below deprecation warnings, be sure to delete this whole class,
    # and the places where it's being used.

    def with_parent_id(self, *args, **kwargs):
        warnings.warn(
            "Using client.payment_chargebacks is deprecated, use "
            "client.chargebacks.with_parent_id(<payment_id>).list() to retrieve Payment chargebacks.",
            RemovedIn215Warning,
        )
        return super().with_parent_id(*args, **kwargs)

    def on(self, *args, **kwargs):
        warnings.warn(
            "Using client.payment_chargebacks is deprecated, use client.chargebacks.on(<payment_object>).list() to "
            "retrieve Payment chargebacks.",
            RemovedIn215Warning,
        )
        return super().on(*args, **kwargs)
