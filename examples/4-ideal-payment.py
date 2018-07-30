# coding=utf-8
#
# Example 4 - How to prepare an iDEAL payment with the Mollie API.
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
        mollie.set_api_key(api_key)

        #
        # First, let the customer pick the bank in a simple HTML form. This step is actually optional.
        #
        if 'issuer' not in flask.request.form:
            body = '<form method="post">Select your bank: <select name="issuer">'
            for issuer in mollie_client.methods.get('ideal', include='issuers').issuers:
                body += '<option value="%s">%s</option>' % (issuer.id, issuer.name)
            body += '<option value="">or select later</option>'
            body += '</select><button>OK</button></form>'
            return body

        else:
            #
            # Get the posted issuer id.
            #
            issuer_id = None

            if flask.request.form['issuer']:
                issuer_id = str(flask.request.form['issuer'])

            #
            # Generate a unique order number for this example. It is important to include this unique attribute
            # in the redirectUrl (below) so a proper return page can be shown to the customer.
            #
            order_id = int(time.time())

            #
            # Payment parameters:
            # amount        Currency and value. This example creates a € 10,- payment.
            # description   Description of the payment.
            # webhookUrl    Webhook location, used to report when the payment changes state.
            # redirectUrl   Redirect location. The customer will be redirected there after the payment.
            # metadata      Custom metadata that is stored with the payment.
            # method        Payment method "ideal".
            # issuer        The customer's bank. If empty the customer can select it later.
            #
            payment = mollie_client.payments.create({
                'amount': {'currency': 'EUR', 'value': '10.00'},
                'description': 'My first API payment',
                'webhookUrl': flask.request.url_root + '2-webhook-verification',
                'redirectUrl': flask.request.url_root + '3-return-page?order_id=' + str(order_id),
                'metadata': {
                    'order_nr': order_id
                },
                'method': 'ideal',
                'issuer': issuer_id
            })

            #
            # In this example we store the order with its payment status in a database.
            #
            database_write(order_id, payment.status)

            #
            # Send the customer off to complete the payment.
            #
            return flask.redirect(payment.checkout_url)

    except mollie.api.error as e:
        return 'API call failed: ' + str(e)


if __name__ == '__main__':
    print(main())
