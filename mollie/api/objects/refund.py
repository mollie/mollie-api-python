from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from .base import ObjectBase
from .list import Collection
from .order_line import OrderLine

if TYPE_CHECKING:
    from ..client import Client
    from ..resources.refunds import Refunds
    from ..typing import Amount
    from .order import Order
    from .payment import Payment


class Refund(ObjectBase):
    @classmethod
    def get_resource_class(cls, client: Client) -> Refunds:
        from ..resources.refunds import Refunds

        return Refunds(client)

    STATUS_QUEUED = "queued"
    STATUS_PENDING = "pending"
    STATUS_PROCESSING = "processing"
    STATUS_REFUNDED = "refunded"

    # documented properties

    @property
    def resource(self) -> str:
        return self._get_property("resource")

    @property
    def id(self) -> str:
        return self._get_property("id")

    @property
    def amount(self) -> Amount:
        return self._get_property("amount")

    @property
    def settlement_amount(self) -> Union[Amount, None]:
        return self._get_property("settlementAmount")

    @property
    def description(self) -> str:
        return self._get_property("description")

    @property
    def status(self) -> str:
        return self._get_property("status")

    @property
    def lines(self) -> Collection:
        """Return the lines for this refund."""
        lines = self._get_property("lines") or []
        result = {
            "_embedded": {
                "lines": lines,
            },
            "count": len(lines),
        }
        return Collection(result, OrderLine, self.client)

    @property
    def payment_id(self) -> str:
        return self._get_property("paymentId")

    @property
    def order_id(self) -> Union[str, None]:
        return self._get_property("orderId")

    @property
    def created_at(self) -> str:
        return self._get_property("createdAt")

    @property
    def metadata(self) -> Union[dict[Any, Any], None]:
        return self._get_property("metadata")

    # documented _links

    @property
    def payment(self) -> Payment:
        """Return the payment for this refund."""
        # TODO refactor this to use the embedded data if possible
        return self.client.payments.get(self.payment_id)

    # @property
    # def settlement(self):
    #     """
    #     Return the settlement for this refund.

    #     TODO: Before we can return an Settlement object, we need to implement the Setlement API.
    #     """
    #     pass

    @property
    def order(self) -> Union[Order, None]:
        """Return the order for this refund."""
        # TODO this might not be availlable
        return self.client.orders.get(self.order_id)

    # additional methods

    def is_queued(self) -> bool:
        return self.status == self.STATUS_QUEUED

    def is_pending(self) -> bool:
        return self.status == self.STATUS_PENDING

    def is_processing(self) -> bool:
        return self.status == self.STATUS_PROCESSING

    def is_refunded(self) -> bool:
        return self.status == self.STATUS_REFUNDED
