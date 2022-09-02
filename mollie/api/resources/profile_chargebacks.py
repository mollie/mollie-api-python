import warnings

from ..error import RemovedIn215Warning
from .chargebacks import Chargebacks


class ProfileChargebacks(Chargebacks):
    # When removing below deprecation warnings, be sure to delete this whole class,
    # and the places where it's being used.

    def with_parent_id(self, *args, **kwargs):
        warnings.warn(
            "Using client.profile_chargebacks is deprecated, use "
            "client.chargebacks.with_parent_id(<profile_id>).list() to retrieve Profile chargebacks.",
            RemovedIn215Warning,
        )
        return super().with_parent_id(*args, **kwargs)

    def on(self, *args, **kwargs):
        warnings.warn(
            "Using client.profile_chargebacks is deprecated, use "
            "client.chargebacks.on(<profile_object>).list() to retrieve Profile chargebacks.",
            RemovedIn215Warning,
        )
        return super().on(*args, **kwargs)
