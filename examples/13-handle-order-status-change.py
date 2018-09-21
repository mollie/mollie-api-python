# coding=utf-8
#
# Example 13 - Handle an order status change using the Mollie API.
#
from __future__ import print_function

import os

from mollie.api.client import Client
from mollie.api.error import Error


def main():
    try:
        #
        # Initialize the Mollie API library with your API key.
        #
        # See: https://www.mollie.com/dashboard/settings/profiles
        #
        api_key = os.environ.get('MOLLIE_API_KEY', 'test_test')
        mollie_client = Client()
        mollie_client.set_api_key(api_key)

        #
        # After your webhook has been called with the order ID in its body, you'd like
        # to handle the order's status change. This is how you can do that.
        #
        # See: https://docs.mollie.com/reference/v2/orders-api/get-order
        #

        order = next(mollie_client.orders.list())
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

    except Error as err:
        return 'API call failed: {error}'.format(error=err)


if __name__ == '__main__':
    print(main())
