from ..error import DataConsistencyError
from ..objects.order_line import OrderLine
from .base import Base


class OrderLines(Base):
    order_id = None

    def get_resource_name(self):
        return 'orders/{order_id}/lines'.format(order_id=self.order_id)

    def get_resource_object(self, result):
        return OrderLine(result, self.client)

    def with_parent_id(self, order_id):
        self.order_id = order_id
        return self

    def on(self, order):
        return self.with_parent_id(order.id)

    def delete(self, data, *args):
        """
        Custom handling for deleting orderlines.

        Orderlines are deleted by issuing a DELETE on the orders/*/lines endpoint,
        with the orderline IDs and quantities in the request body.
        """
        path = self.get_resource_name()
        result = self.perform_api_call(self.REST_DELETE, path, data=data)
        return result

    def update(self, resource_id, data=None, **params):
        """
        Custom handling for updating orderlines.

        The API returns an Order object. Since we are sending the request through an orderline object, it makes more
        sense to convert the returned object to to the updated orderline object.

        If you wish to retrieve the order object, you can do so by using the order_id property of the orderline.
        """
        path = self.get_resource_name() + '/' + str(resource_id)
        result = self.perform_api_call(self.REST_UPDATE, path, data=data)

        for line in result['lines']:
            if line['id'] == resource_id:
                return self.get_resource_object(line)
        raise DataConsistencyError('Line id {resource_id} not found in response.'.format(resource_id=resource_id))
