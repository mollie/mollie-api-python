from .refunds import Refunds


class OrderRefunds(Refunds):
    order_id = None

    def get_resource_name(self):
        return 'orders/{id}/refunds'.format(id=self.order_id)

    def with_parent_id(self, order_id):
        self.order_id = order_id
        return self

    def on(self, order):
        return self.with_parent_id(order.id)
