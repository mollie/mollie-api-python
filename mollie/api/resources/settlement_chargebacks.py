import warnings

from ..error import RemovedIn215Warning
from .chargebacks import Chargebacks


class SettlementChargebacks(Chargebacks):
    def with_parent_id(self, *args, **kwargs):
        warnings.warn(
            "Using client.settlement_chargebacks is deprecated, use "
            "client.chargebacks.with_parent_id(<settlement_id>).list() to retrieve Settlement chargebacks.",
            RemovedIn215Warning,
        )

        return super().with_parent_id(*args, **kwargs)

    def on(self, *args, **kwargs):
        warnings.warn(
            "Using client.settlement_chargebacks is deprecated, use "
            "client.chargebacks.on(<settlement_object>).list() to retrieve Settlement chargebacks.",
            RemovedIn215Warning,
        )

        return super().on(*args, **kwargs)
