from ..error import IdentifierError
from ..objects.order import Order
from .base import Base


class Orders(Base):
    RESOURCE_ID_PREFIX = 'ord_'

    def get_resource_object(self, result):
        return Order(result, client=self.client)

    def get(self, order_id, **params):
        if not order_id or not order_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                "Invalid order ID: '{id}'. An order ID should start with '{prefix}'.".format(
                    id=order_id, prefix=self.RESOURCE_ID_PREFIX)
            )
        return super(Orders, self).get(order_id, **params)

    def delete(self, order_id, data=None):
        """Cancel order and return the order object.

        Deleting an order causes the order status to change to canceled.
        The updated order object is returned.
        """
        if not order_id or not order_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                "Invalid order ID: '{id}'. An order ID should start with '{prefix}'.".format(
                    id=order_id, prefix=self.RESOURCE_ID_PREFIX)
            )
        result = super(Orders, self).delete(order_id, data)
        return self.get_resource_object(result)
