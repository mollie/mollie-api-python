from .payments import Payments


class OrderPayments(Payments):
    order_id = None

    def get_resource_name(self):
        return 'orders/{id}/payments'.format(id=self.order_id)

    def with_parent_id(self, order_id):
        self.order_id = order_id
        return self

    def on(self, order):
        return self.with_parent_id(order.id)
