# coding=utf-8
#
# Example 15 - List orders using the Mollie API.
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
        # Cancel the order with ID "ord_pbjz8x
        #
        # See: https://docs.mollie.com/reference/v2/orders-api/cancel-order
        #

        body = ''
        orders = mollie_client.orders.list()
        if not len(orders):
            body += '<p>You have no orders. You can create one from the examples.</p>'
            return body

        for order in orders:
            body += '<li><b>Order {order_id}:</b> ({created_at})'.format(order_id=order.id,
                                                                         created_at=order.created_at)
            body += '<b>Status: </b>{status}'.format(status=order.status)
            body += '<table border="1"><tr><th>Billed to</th><th>Shipped to</th><th>Total amount</th></tr>'
            body += '<tr>'
            body += '<td>{shipping_given_name} {shipping_family_name}</td>'.format(
                shipping_given_name=order.shipping_address['givenName'],
                shipping_family_name=order.shipping_address['familyName'])
            body += '<td>{billing_given_name} {billing_family_name}</td>'.format(
                billing_given_name=order.billing_address['givenName'],
                billing_family_name=order.billing_address['familyName'])
            body += '<td>{currency} {value}</td>'.format(currency=order.amount['currency'],
                                                         value=order.amount['value'])
            body += '</tr>'
            body += '</table>'
            body += '<a href="{checkout_url}" target="_blank">Click here to pay</a>'.format(
                checkout_url=order.checkout_url)
            body += '</li>'
            return body

    except Error as err:
        return 'API call failed: {error}'.format(error=err)


if __name__ == '__main__':
    print(main())
