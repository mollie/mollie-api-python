# coding=utf-8
#
# Example 1 - How to prepare a new payment with the Mollie API.
#
from __future__ import print_function

import sys, os, time, flask
from app import database_write

#
# Add Mollie library to module path so we can import it.
# This is not necessary if you use pip or easy_install.
#
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))

import Mollie


def main():
    try:
        #
        # Initialize the Mollie API library with your API key.
        #
        # See: https://www.mollie.nl/beheer/account/profielen/
        #
        mollie = Mollie.API.Client()
        mollie.setApiKey('test_bt7vvByF6jTcBR4dLuW66eNnHYNIJp')

        #
        # Generate a unique order number for this example. It is important to include this unique attribute
        # in the redirectUrl (below) so a proper return page can be shown to the customer.
        #
        order_nr = int(time.time())

        #
        # Payment parameters:
        # amount        Amount in EUROs. This example creates a € 10,- payment.
        # description   Description of the payment.
        # redirectUrl   Redirect location. The customer will be redirected there after the payment.
        # metadata      Custom metadata that is stored with the payment.
        #
        payment = mollie.payments.create({
            'amount': 10.00,
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

    except Mollie.API.Error as e:
        return 'API call failed: ' + e.message


if __name__ == '__main__':
    print(main())
