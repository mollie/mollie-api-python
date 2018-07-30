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
            'from': 0,
            'count': amount_of_payments_to_retrieve,
        }
        payments = mollie_client.customer_payments.with_parent_id(customer_id).all(**params)

        body += '<p>Customer "%s" has %s payments</p>' % (customer.id, payments.count)

        if int(payments.count) > amount_of_payments_to_retrieve:
            body += '<p><b>Note: Only showing first %s payments</b></p>' % amount_of_payments_to_retrieve

        for payment in payments:
            body += "<p>Payment %s (%s) %s</p>" % (payment.id, payment.amount['value'], payment.amount['currency'])

        return body

    except mollie.api.error as e:
        return 'API call failed: ' + str(e)


if __name__ == '__main__':
    print(main())
