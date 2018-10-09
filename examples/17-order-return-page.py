#
# Example: How to show a return page to the customer.
#
# In this example we retrieve the order stored in the database.
#
from __future__ import print_function

import os

import flask

from app import database_read
from mollie.api.client import Client


def main():
    api_key = os.environ.get('MOLLIE_API_KEY', 'test_test')
    mollie_client = Client()
    mollie_client.set_api_key(api_key)

    if 'my_webshop_id' not in flask.request.args:
        flask.abort(404, 'Unknown webshop id')

    data = database_read(flask.request.args['my_webshop_id'])

    order = mollie_client.orders.get(data['order_id'])

    if order.is_paid():
        return 'The payment for your order {order_id} has been processed'.format(order_id=order.id)

    elif order.is_canceled():
        return 'Your order {order_id} has been canceled'.format(order_id=order.id)

    elif order.is_shipping():
        return 'Your order {order_id} is shipping'.format(order_id=order.id)

    elif order.is_created():
        return 'Your order {order_id} has been created'.format(order_id=order.id)

    elif order.is_authorized():
        return 'Your order {order_id} is authorized'.format(order_id=order.id)

    elif order.is_refunded():
        return 'Your order {order_id} has been refunded'.format(order_id=order.id)

    elif order.is_expired():
        return 'Your order {order_id} has expired'.format(order_id=order.id)

    elif order.is_completed():
        return 'Your order {order_id} is completed'.format(order_id=order.id)

    else:
        return 'The status of your order {order_id} is: {status}'.format(order_id=order.id, status=order.status)


if __name__ == '__main__':
    print(main())
