# coding=utf-8
#
# Example: Retrieve a shipment using the Mollie API.
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
        # Retrieve the first shipment for your first order
        #
        # See: https://docs.mollie.com/reference/v2/shipments-api/get-shipment
        #
        body = '<p>Attempting to retrieve the first page of orders and grabbing the first.</p>'

        order = next(mollie_client.orders.list())
        if not len(order.shipments):
            body += '<p>You have no shipments. You can create one from the examples.</p>'
            return body

        shipment = next(order.shipments)
        body += 'Shipment with ID {shipment_id} for order with ID {order_id}'.format(
            shipment_id=shipment.id, order_id=order.id)

        for line in shipment.lines:
            body += '{name} Status: <b>{status}</b>'.format(name=line.name, status=line.status)

        return body
    except Error as err:
        return 'API call failed: {error}'.format(error=err)


if __name__ == '__main__':
    print(main())
