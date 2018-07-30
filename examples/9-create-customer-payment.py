# coding=utf-8
#
#  Example 9 - Creating a payment for a customer
#
from __future__ import print_function

import os
import time

import flask

import mollie
from app import database_write


def main():
    try:
        #
        # Initialize the Mollie API library with your API key.
        #
        # See: https://www.mollie.com/dashboard/settings/profiles
        #
        api_key = os.environ.get('MOLLIE_API_KEY', 'test_test')
        mollie_client = mollie.api.client.Client()
        mollie_client.set_api_key(api_key)

        body = ''

        customer_id = flask.request.args.get('customer_id')

        # If no customer ID was provided in the URL, we grab the first customer
        if customer_id is None:
            customers = mollie_client.customers.all()

            body += '<p>No customer ID specified. Attempting to retrieve all customers and grabbing the first.</p>'

            if int(customers.count) == 0:
                body += '<p>You have no customers. You can create one from the examples.</p>'
                return body

            for customer in customers:
                customer_id = customer.id
                break

        customer = mollie_client.customers.get(customer_id)

        #
        # Generate a unique order number for this example. It is important to include this unique attribute
        # in the redirectUrl (below) so a proper return page can be shown to the customer.
        #
        order_id = int(time.time())

        #
        # See: https://www.mollie.com/nl/docs/reference/customers/create-payment
        #
        payment = mollie_client.customer_payments.with_parent_id(customer_id).create({
            'amount': {'currency': 'EUR', 'value': '100.00'},
            'description': 'My first API payment',
            'webhookUrl': flask.request.url_root + '2-webhook-verification',
            'redirectUrl': flask.request.url_root + '3-return-page?order_id=' + str(order_id),
            'metadata': {
                'order_id': order_id
            }
        })

        database_write(order_id, payment.status)

        return '<p>Created payment of %s %s for %s (%s)<p>' % (
            payment.value, payment.currency, customer.name, customer.id)

    except mollie.api.error as e:
        return 'API call failed: ' + str(e)


if __name__ == '__main__':
    print(main())
