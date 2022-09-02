import warnings

from ..error import RemovedIn215Warning
from .captures import Captures


class SettlementCaptures(Captures):
    # When removing below deprecation warnings, be sure to delete this whole class,
    # and the places where it's being used.

    def with_parent_id(self, *args, **kwargs):
        warnings.warn(
            "Using client.settlement_captures is deprecated, use "
            "client.captures.with_parent_id(<settlement_id>).list() to retrieve Settlement captures.",
            RemovedIn215Warning,
        )
        return super().with_parent_id(*args, **kwargs)

    def on(self, *args, **kwargs):
        warnings.warn(
            "Using client.settlement_captures is deprecated, use client.captures.on(<settlement_object>).list() to "
            "retrieve Settlement captures.",
            RemovedIn215Warning,
        )
        return super().on(*args, **kwargs)
