# coding=utf-8
#
# Example 20 - Retrieve a list of shipments using the Mollie API.
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
        #

        api_key = os.environ.get('MOLLIE_API_KEY', 'test_test')
        mollie_client = Client()
        mollie_client.set_api_key(api_key)

        #
        # Listing shipments for the first order.
        #
        # See: https://docs.mollie.com/reference/v2/shipments-api/get-shipment
        #
        body = ''

        order = next(mollie_client.orders.list())
        shipments = order.shipments

        body += 'Shipments for order with ID {order_id}:'.format(order_id=order.id)
        for shipment in shipments:
            body += 'Shipment {shipment_id} Items:'
            for line in shipment.lines:
                body += '{name} Status: <b> {status}</b>'.format(name=line.description, status=line.status)
        return body
    except Error as err:
        return 'API call failed: {error}'.format(error=err)


if __name__ == '__main__':
    print(main())
