# coding=utf-8
#
# Example 12 - How to prepare a new order with the Mollie API.
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
        # Order creation parameters.
        #
        # See: https://docs.mollie.com/reference/v2/orders-api/create-order
        #

        order = mollie_client.orders.create({
            'amount': {
                'value': '299.00',
                'currency': 'EUR'
            },
            'billingAddress': {
                'streetAndNumber': 'Keizersgracht 313',
                'city': 'Amsterdam',
                'region': 'Noord-Holland',
                'postalCode': '1234AB',
                'country': 'NL',
                'givenName': 'Piet',
                'familyName': 'Mondriaan',
                'email': 'piet@mondriaan.com',
            },
            'shippingAddress': {
                'streetAndNumber': 'Prinsengracht 313',
                'city': 'Haarlem',
                'region': 'Noord-Holland',
                'postalCode': '5678AB',
                'country': 'NL',
                'givenName': 'Chuck',
                'familyName': 'Norris',
                'email': 'norris@chucknorrisfacts.net'
            },
            'metadata': {
                'order_id': '1337',
                'description': 'Lego cars'
            },
            'consumerDateOfBirth': '1958-01-31',
            'locale': 'nl_NL',
            'orderNumber': '1337',
            'redirectUrl': 'https://example.org/redirect',
            'webhookUrl': 'https://example.org/webhook',
            'method': 'ideal',
            'lines': [
                {
                    'type': 'physical',
                    'sku': '5702016116977',
                    'name': 'LEGO 42083 Bugatti Chiron',
                    'productUrl': 'https://shop.lego.com/nl-NL/Bugatti-Chiron-42083',
                    'imageUrl': 'https://sh-s7-live-s.legocdn.com/is/image//LEGO/42083_alt1?$main$',
                    'quantity': 1,
                    'vatRate': '21.00',
                    'unitPrice': {
                        'currency': 'EUR',
                        'value': '399.00'
                    },
                    'totalAmount': {
                        'currency': 'EUR',
                        'value': '299.00'
                    },
                    'discountAmount': {
                        'currency': 'EUR',
                        'value': '100.00'
                    },
                    'vatAmount': {
                        'currency': 'EUR',
                        'value': '51.89'
                    }
                },

            ]
        })
        database_write(order.metadata['order_id'], order.status)

        #
        # Send the customer off to complete the order payment.
        #
        return flask.redirect(order.checkout_url)

    except Error as err:
        return 'API call failed: {error}'.format(error=err)


if __name__ == '__main__':
    print(main())
