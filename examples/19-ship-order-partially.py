# coding=utf-8
#
# Example: Create a shipment for part of an order using the Mollie API.
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
        # Create a shipment for the first line of your first order
        #
        # See: https://docs.mollie.com/reference/v2/shipments-api/create-shipment
        #

        body = '<p>Attempting to retrieve the first page of orders and grabbing the first.</p>'
        order = next(mollie_client.orders.list())
        line = next(order.lines)
        data = {
            'lines': [
                {
                    'id': line.id,
                }
            ],
            'tracking': {
                'carrier': 'PostNL',
                'code': '3SKABA000000000',
                'url': 'http://postnl.nl/tracktrace/?B=3SKABA000000000&P=1016EE&D=NL&T=C'
            },
        }
        shipment = order.create_shipment(data)
        body += 'A shipment with ID {shipment_id} has been created for your order with ID {order_id}'.format(
            shipment_id=shipment.id, order_id=order.id)

        return body
    except Error as err:
        return 'API call failed: {error}'.format(error=err)


if __name__ == '__main__':
    print(main())
