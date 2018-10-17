# coding=utf-8
#
#  Example: Creating a payment for a customer
#
from __future__ import print_function

import os
import time

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

        body = ''

        customer_id = flask.request.args.get('customer_id')

        # If no customer ID was provided in the URL, we grab the first customer
        if customer_id is None:
            customers = mollie_client.customers.list()

            body += '<p>No customer ID specified. Attempting to retrieve the first page of '
            body += 'customers and grabbing the first.</p>'

            if not len(customers):
                body += '<p>You have no customers. You can create one from the examples.</p>'
                return body

            customer = next(customers)
        else:
            customer = mollie_client.customers.get(customer_id)

        #
        # Generate a unique webshop order number for this example. It is important to include this unique attribute
        # in the redirectUrl (below) so a proper return page can be shown to the customer.
        #
        my_webshop_id = int(time.time())

        #
        # See: https://www.mollie.com/nl/docs/reference/customers/create-payment
        #
        payment = mollie_client.customer_payments.with_parent_id(customer.id).create({
            'amount': {
                'currency': 'EUR',
                'value': '100.00'
            },
            'description': 'My first API payment',
            'webhookUrl': '{root}02-webhook_verification'.format(root=flask.request.url_root),
            'redirectUrl': '{root}03-return-page?my_webshop_id={id}'.format(
                root=flask.request.url_root, id=my_webshop_id),
            'metadata': {
                'my_webshop_id': str(my_webshop_id)
            },
        })
        data = {'status': payment.status}
        database_write(my_webshop_id, data)

        return '<p>Created payment of {curr} {value} for {cust} ({id})<p>'.format(
            curr=payment.amount['currency'], value=payment.amount['value'], cust=customer.name, id=customer.id)

    except Error as err:
        return 'API call failed: {error}'.format(error=err)


if __name__ == '__main__':
    print(main())
