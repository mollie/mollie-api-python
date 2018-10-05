# coding=utf-8
#
# Example: List orders using the Mollie API.
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
        # List the most recent orders
        #
        # See: https://docs.mollie.com/reference/v2/orders-api/list-orders
        #
        body = ''
        orders = mollie_client.orders.list()
        if not len(orders):
            body += '<p>You have no orders. You can create one from the examples.</p>'
            return body

        body += '<p>Showing the last {num} orders for your API key.</p>'.format(num=len(orders))

        body += """
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Billed to</th>
                        <th>Shipped to</th>
                        <th>Total amount</th>
                    </tr>
                </thead>
                <tbody>
        """

        for order in orders:
            body += '<tr>'
            body += '<td>{id}</td>'.format(id=order.id)
            body += '<td>{billing_given_name} {billing_family_name}</td>'.format(
                billing_given_name=order.billing_address['givenName'],
                billing_family_name=order.billing_address['familyName'])
            body += '<td>{shipping_given_name} {shipping_family_name}</td>'.format(
                shipping_given_name=order.shipping_address['givenName'],
                shipping_family_name=order.shipping_address['familyName'])
            body += '<td>{currency} {value}</td>'.format(currency=order.amount['currency'],
                                                         value=order.amount['value'])
            body += '<td><a href="{checkout_url}" target="_blank">Pay order</a></td>'.format(
                checkout_url=order.checkout_url)
            body += '<td><a href="/14-cancel-order?order_id={id}">Cancel order</a></td>'.format(
                id=order.id)
            body += '<td><a href="/18-ship-order-completely?order_id={id}">Ship order</a></td>'.format(
                id=order.id)
            body += '</tr>'

        body += "</tbody></table>"
        return body

    except Error as err:
        return 'API call failed: {error}'.format(error=err)


if __name__ == '__main__':
    print(main())
