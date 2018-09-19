# coding=utf-8
#
# Example 14 - Cancel an order using the Mollie API.
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
        # Cancel the order with ID "ord_pbjz8x
        #
        # See: https://docs.mollie.com/reference/v2/orders-api/cancel-order
        #

        order = mollie_client.orders.get('ord_pbjz8x')
        if order.is_cancelable:
            mollie_client.orders.delete(order.id)
            return 'Your order {order_id} has been canceled'.format(order_id=order.id)

        else:
            return 'Unable to cancel your order {order_id}'.format(order_id=order.id)

    except Error as err:
        return 'API call failed: {error}'.format(error=err)


if __name__ == '__main__':
    print(main())
