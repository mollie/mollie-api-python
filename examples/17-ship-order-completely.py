# coding=utf-8
#
# Example 17 - Create a shipment for an entire order using the Mollie API.
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
        # Create a shipment for your entire first order
        #
        # See: https://docs.mollie.com/reference/v2/shipments-api/create-shipment
        #

        body = ''
        order = next(mollie_client.orders.list())
        shipment = order.create_shipment()
        body += 'A shipment with ID {shipment_id} has been created for your order with ID {order_id}'.format(
            shipment_id=shipment.id, order_id=order.id)
        for line in shipment.lines:
            body += '{name} Status: <b>{status}</b>'.format(name=line.name, status=line.status)

        return body
    except Error as err:
        return 'API call failed: {error}'.format(error=err)


if __name__ == '__main__':
    print(main())
