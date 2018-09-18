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
