# coding=utf-8
#
# Example 16 - Cancel an order line using the Mollie API.
#
from __future__ import print_function

import os

from mollie.api.client import Client
from mollie.api.error import Error


def main():
    try:
        #
        # List the most recent orders
        #
        # See: https://docs.mollie.com/reference/v2/orders-api/list-orders
        #
        api_key = os.environ.get('MOLLIE_API_KEY', 'test_test')
        mollie_client = Client()
        mollie_client.set_api_key(api_key)

        #
        # Cancel an order line with ID "odl_dgtxyl" for order ID "ord_8wmqcHMN4U"
        #
        # See: https://docs.mollie.com/reference/v2/orders-api/cancel-order-line
        #

        order_id = 'ord_8wmqcHMN4U'
        line_id = 'odl_dgtxyl'

        order = mollie_client.orders.get(order_id)
        lines = order.order_lines.get(line_id)
        line = next(lines)
        body = ''
        if line and line.is_cancelable:
            line.cancel()

            order = mollie_client.orders.get(order_id)
            body += 'Your order {order_id} was updated:'.format(order_id=order.id)
            for line in order.order_lines:
                body += '{name} Status: <b>{status}</b>'.format(name=line.name, status=line.status)
        else:
            body += 'Unable to cancel line {line_id} for your order {order_id}'.format(line_id=line_id,
                                                                                       order_id=order_id)

    except Error as err:
        return 'API call failed: {error}'.format(error=err)


if __name__ == '__main__':
    print(main())
