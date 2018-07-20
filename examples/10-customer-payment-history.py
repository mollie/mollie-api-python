# coding=utf-8
#
#  Example 10 - Retrieving the payment history for a customer
#
from __future__ import print_function

import os

import flask

import mollie


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

        body = ''

        customer_id = flask.request.args.get('customer_id')

        # If no customer ID was provided in the URL, we grab the first customer
        if customer_id is None:
            customers = mollie_client.customers.all()

            body += '<p>No customer ID specified. Attempting to retrieve all customers and grabbing the first.</p>'

            if int(customers['totalCount']) == 0:
                body += '<p>You have no customers. You can create one from the examples.</p>'
                return body

            for customer in customers:
                customer_id = customer['id']
                break

        customer = mollie_client.customers.get(customer_id)

        amount_of_payments_to_retrieve = 20

        #
        # Retrieve the latest payments for the customer
        #
        # See: https://www.mollie.com/nl/docs/reference/customers/list-payments
        #
        payments = mollie_client.customer_payments.withParentId(customer_id).all(offset=0, count=amount_of_payments_to_retrieve)

        body += '<p>Customer "%s" has %s payments</p>' % (customer['id'], payments['totalCount'])

        if int(payments['totalCount']) > amount_of_payments_to_retrieve:
            body += '<p><b>Note: Only showing first %s payments</b></p>' % amount_of_payments_to_retrieve

        for payment in payments:
            body += "<p>Payment %s (%s) EUR</p>" % (payment['id'], payment['amount'])

        return body

    except mollie.api.error as e:
        return 'API call failed: ' + str(e)


if __name__ == '__main__':
    print(main())
