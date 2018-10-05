# coding=utf-8
#
# Example: Cancel an order using the Mollie API.
#
from __future__ import print_function

import os

import flask

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
        # Cancel the order.
        #
        # See: https://docs.mollie.com/reference/v2/orders-api/cancel-order
        #
        body = ''

        order_id = flask.request.args.get('order_id')

        if order_id is None:
            body += '<p>No order ID specified. Attempting to retrieve the first page of '
            body += 'orders and grabbing the first.</p>'

        order = mollie_client.orders.get(order_id) if order_id else next(mollie_client.orders.list())

        if order.is_cancelable:
            mollie_client.orders.delete(order.id)
            body += 'Your order {order_id} has been canceled'.format(order_id=order.id)

        else:
            body += 'Unable to cancel your order {order_id}'.format(order_id=order.id)

        return body

    except Error as err:
        return 'API call failed: {error}'.format(error=err)


if __name__ == '__main__':
    print(main())
