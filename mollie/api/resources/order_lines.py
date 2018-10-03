from ..objects.order_line import OrderLine
from .base import Base


class OrderLines(Base):
    order_id = None

    def get_resource_object(self, result):
        return OrderLine(result, client=self.client)

    def with_parent_id(self, order_id):
        self.order_id = order_id
        return self

    def get_resource_name(self):
        return 'orders/{order_id}/lines'.format(order_id=self.order_id)

    def on(self, order):
        return self.with_parent_id(order.id)

    def delete(self, data):
        # Delete function on the parent ID without own id
        path = self.get_resource_name()
        result = self.perform_api_call(self.REST_DELETE, path, data=data)
        return self.get_resource_object(result)
