# coding=utf-8
#
# Example: Retrieve a list of shipments using the Mollie API.
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
        # See: https://docs.mollie.com/reference/v2/shipments-api/list-shipments
        #
        body = '<p>Attempting to retrieve the first page of orders, and grabbing the first.</p>'
        order = next(mollie_client.orders.list())
        shipments = order.shipments

        body += 'Shipments for order with ID {order_id}:'.format(order_id=order.id)
        body += """
            <table>
                <thead>
                    <tr>
                        <th>Shipment ID</th>
                        <th>Tracking url</th>
                        <th>Created at</th>
                    </tr>
                </thead>
                <tbody>
        """
        for shipment in shipments:
            body += '<tr>'
            body += '<td>{id}</td>'.format(id=shipment.id)
            body += '<td>{url}</td>'.format(url=shipment.tracking_url)
            body += '<td>{created}</td>'.format(created=shipment.created_at)
            body += '</tr>'

        body += "</tbody></table>"

        return body
    except Error as err:
        return 'API call failed: {error}'.format(error=err)


if __name__ == '__main__':
    print(main())
