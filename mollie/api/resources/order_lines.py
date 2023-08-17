from typing import TYPE_CHECKING, Any, Dict, Optional

from ..error import DataConsistencyError
from ..objects.list import PaginationList
from ..objects.order_line import OrderLine
from .base import ResourceBase

if TYPE_CHECKING:
    from ..client import Client
    from ..objects.order import Order

__all__ = [
    "OrderLines",
]


class OrderLines(ResourceBase):
    """
    Resource handler for the `/orders/:order_id:/lines` endpoint.

    This class provides various generic methods such as .delete(), .update() and
    .list(), but since the API interface for these methods is completely different
    from other endpoints, all methods don't use the generic methods but have custom
    implementations in this class.
    """

    RESOURCE_ID_PREFIX: str = "odl_"
    object_type = OrderLine

    _order: "Order"

    def __init__(self, client: "Client", order: "Order") -> None:
        self._order = order
        super().__init__(client)

    def get_resource_path(self) -> str:
        return f"orders/{self._order.id}/lines"

    def delete_lines(self, data: Optional[Dict[str, Any]] = None, **params: Any) -> dict:
        """
        Cancel multiple orderlines.

        Orderlines are (partially) canceled by sending a list of lines with id's and
        optionally altered properties to the API. See the Mollie docs for details.

            data = {
                "lines":
                    [
                        {
                            "id": 'odl_dgtxyl',
                            "quantity": 1,
                        }
                    ]
                }
            order.lines.delete_lines(data)

        To cancel all lines, simply omit the data parameter.

            order.lines.delete_lines()

        Note: since this differs significantly from a regular .delete(), the method
        has a different name.
        """
        if data is None:
            data = {"lines": []}

        path = self.get_resource_path()
        return self.perform_api_call(self.REST_DELETE, path, data=data, params=params)

    def delete(self, order_line_id: str, **params: Any) -> dict:
        """
        Cancel a single orderline.

        This method provides the regular .delete() interface on top of .delete_lines().
        """
        self.validate_resource_id(order_line_id, "orderline ID")
        data = {
            "lines": [
                {"id": order_line_id},
            ],
        }
        return self.delete_lines(data, **params)

    def update(self, order_line_id: str, data: Optional[Dict[str, Any]] = None, **params: Any) -> OrderLine:
        """
        Custom handling for updating orderlines.

        We are manipulating an orderline here, but the API returns the full order payload.
        To be more consistent, we return the updated orderline object in stead.

        If you wish to retrieve the order object, you can do so by using the order_id property of the orderline.
        """
        resource_path = self.get_resource_path()
        path = f"{resource_path}/{order_line_id}"
        result = self.perform_api_call(self.REST_UPDATE, path, data=data, params=params)

        for line in result["lines"]:
            if line["id"] == order_line_id:
                return OrderLine(line, self.client)

        raise DataConsistencyError(f"OrderLine with id '{order_line_id}' not found in response.")

    def list(self, **params: Any) -> PaginationList:
        """Return the orderline data from the related order."""
        lines = self._order._get_property("lines") or []
        data = {
            "_embedded": {
                "lines": lines,
            },
            "count": len(lines),
        }
        return PaginationList(data, self, self.client)
