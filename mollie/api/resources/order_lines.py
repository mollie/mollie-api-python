from ..objects.order_line import OrderLine
from .base import Base


class OrderLines(Base):
    order_id = None

    def get_resource_name(self):
        return 'orders/{order_id}/lines'.format(order_id=self.order_id)

    def get_resource_object(self, result):
        return OrderLine(result, client=self.client)

    def with_parent_id(self, order_id):
        self.order_id = order_id
        return self

    def on(self, order):
        return self.with_parent_id(order.id)

    def delete(self, data, *args):
        """
        Custom handling for deleting orderlines.

        Orderlines are deleted by issueing a DELETE on the orders/*/lines endpoint,
        with the orderline IDs and quantities in the request body.
        """
        path = self.get_resource_name()
        result = self.perform_api_call(self.REST_DELETE, path, data=data)
        return result
