# coding=utf-8
#
#  Example: Retrieving the payment history for a customer
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
            customers = mollie_client.customers.list()

            body += '<p>No customer ID specified. Attempting to retrieve the first page of customers '
            body += 'and grabbing the first.</p>'

            if not len(customers):
                body += '<p>You have no customers. You can create one from the examples.</p>'
                return body

            customer = next(customers)
        else:
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
        payments = mollie_client.customer_payments.with_parent_id(customer.id).list(**params)

        body += '<p>Showing the last {num} payments for customer "{cust}"</p>'.format(
            num=len(payments), cust=customer.id)

        for payment in payments:
            body += "<p>Payment {id} ({value}) {curr}</p>".format(
                id=payment.id, value=payment.amount['value'], curr=payment.amount['currency'])
        return body

    except Error as err:
        return 'API call failed: {error}'.format(error=err)


if __name__ == '__main__':
    print(main())
