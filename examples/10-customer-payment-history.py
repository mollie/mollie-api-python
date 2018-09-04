# coding=utf-8
#
#  Example 10 - Retrieving the payment history for a customer
#
from __future__ import print_function

import os

import flask

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
            customers = mollie_client.customers.all()

            body += '<p>No customer ID specified. Attempting to retrieve all customers and grabbing the first.</p>'

            if int(customers.count) == 0:
                body += '<p>You have no customers. You can create one from the examples.</p>'
                return body

            for customer in customers:
                customer_id = customer.id
                break

        customer = mollie_client.customers.get(customer_id)

        amount_of_payments_to_retrieve = 20

        #
        # Retrieve the latest payments for the customer
        #
        # See: https://www.mollie.com/nl/docs/reference/customers/list-payments
        #
        params = {
            'limit': amount_of_payments_to_retrieve,
        }
        payments = mollie_client.customer_payments.with_parent_id(customer_id).all(**params)

        body += '<p>Showing the last %s payments for customer "%s"</p>' % (payments.count, customer.id)

        for payment in payments:
            body += "<p>Payment %s (%s) %s</p>" % (payment.id, payment.amount['value'], payment.amount['currency'])

        return body

    except Error as err:
        return 'API call failed: %s' % err


if __name__ == '__main__':
    print(main())
