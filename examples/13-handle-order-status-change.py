# coding=utf-8
#
# Example 13 - Handle an order status change using the Mollie API.
#
from __future__ import print_function

import os

import flask

from app import database_write
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
        if 'id' not in flask.request.form:
            flask.abort(404, 'Unknown payment id')

        order_id = flask.request.form['id']
        order = mollie_client.orders.get(order_id)
        my_webshop_id = order.metadata['my_webshop_id']

        #
        # Update the order in the database.
        #
        data = {'order_id': order.id, 'status': order.status}
        database_write(my_webshop_id, data)

    except Error as err:
        return 'API call failed: {error}'.format(error=err)


if __name__ == '__main__':
    print(main())
