#
# Example 2 - How to verify Mollie API Payments in a webhook.
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
        # Retrieve the payment's current state.
        #
        if 'id' not in flask.request.form:
            flask.abort(404, 'Unknown payment id')

        payment_id = flask.request.form['id']
        payment = mollie_client.payments.get(payment_id)
        my_webshop_id = payment.metadata['my_webshop_id']

        #
        # Update the order in the database.
        #
        data = {'status': payment.status}
        database_write(my_webshop_id, data)

        #
        # When your payment status is paid,
        # you'd probably want to start the process of delivering the product to the owner
        #

    except Error as err:
        return 'API call failed: {error}'.format(error=err)


if __name__ == '__main__':
    print(main())
