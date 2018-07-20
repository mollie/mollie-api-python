# coding=utf-8
#
# Example 1 - How to prepare a new payment with the Mollie API.
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
        mollie_client = mollie.api.Client()
        mollie_client.setApiKey(api_key)

        #
        # Generate a unique order number for this example. It is important to include this unique attribute
        # in the redirectUrl (below) so a proper return page can be shown to the customer.
        #
        order_nr = int(time.time())

        #
        # Payment parameters:
        # amount        Amount in EUROs. This example creates a € 10,- payment.
        # description   Description of the payment.
        # webhookUrl    Webhook location, used to report when the payment changes state.
        # redirectUrl   Redirect location. The customer will be redirected there after the payment.
        # metadata      Custom metadata that is stored with the payment.
        #
        payment = mollie_client.payments.create({
            'amount':      10.00,
            'description': 'My first API payment',
            'webhookUrl':  flask.request.url_root + '2-webhook-verification?order_nr=' + str(order_nr),
            'redirectUrl': flask.request.url_root + '3-return-page?order_nr=' + str(order_nr),
            'metadata': {
                'order_nr': order_nr
            }
        })

        #
        # In this example we store the order with its payment status in a database.
        #
        database_write(order_nr, payment['status'])

        #
        # Send the customer off to complete the payment.
        #
        return flask.redirect(payment.getPaymentUrl())

    except mollie.api.Error as e:
        return 'API call failed: ' + str(e)


if __name__ == '__main__':
    print(main())
