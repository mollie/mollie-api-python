#
# Example 2 - How to verify Mollie API Payments in a webhook.
#
from __future__ import print_function

import os

import flask

import Mollie
from app import database_write


def main():
    try:
        #
        # Initialize the Mollie API library with your API key.
        #
        # See: https://www.mollie.com/dashboard/settings/profiles
        #
        api_key = os.environ.get('MOLLIE_API_KEY', 'test_test')
        mollie = Mollie.API.Client()
        mollie.setApiKey(api_key)

        #
        # Retrieve the payment's current state.
        #
        if 'id' not in flask.request.form:
            flask.abort(404, 'Unknown payment id')

        payment_id = flask.request.form['id']
        payment = mollie.payments.get(payment_id)
        order_nr = payment['metadata']['order_nr']

        #
        # Update the order in the database.
        #
        database_write(order_nr, payment['status'])

        if payment.isPaid():
            #
            # At this point you'd probably want to start the process of delivering the product to the customer.
            #
            return 'Paid'
        elif payment.isPending():
            #
            # The payment has started but is not complete yet.
            #
            return 'Pending'
        elif payment.isOpen():
            #
            # The payment has not started yet. Wait for it.
            #
            return 'Open'
        else:
            #
            # The payment isn't paid, pending nor open. We can assume it was aborted.
            #
            return 'Cancelled'

    except Mollie.API.Error as e:
        return 'API call failed: ' + str(e)


if __name__ == '__main__':
    print(main())
