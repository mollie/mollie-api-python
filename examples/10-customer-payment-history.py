# coding=utf-8
#
#  Example 10 - Retrieving the payment history for a customer
#
from __future__ import print_function

import sys, os, flask

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
        # See: https://www.mollie.com/dashboard/settings/profiles
        #
        mollie = Mollie.API.Client()
        mollie.setApiKey('test_bt7vvByF6jTcBR4dLuW66eNnHYNIJp')

        body = ''

        customer_id = flask.request.args.get('customer_id')

        # If no customer ID was provided in the URL, we grab the first customer
        if customer_id is None:
            customers = mollie.customers.all()

            body += '<p>No customer ID specified. Attempting to retrieve all customers and grabbing the first.</p>'

            if int(customers['totalCount']) == 0:
                body += '<p>You have no customers. You can create one from the examples.</p>'
                return body

            for customer in customers:
                customer_id = customer['id']
                break

        customer = mollie.customers.get(customer_id)

        amount_of_payments_to_retrieve = 20

        #
        # Retrieve the latest payments for the customer
        #
        # See: https://www.mollie.com/nl/docs/reference/customers/list-payments
        #
        payments = mollie.customer_payments.withParentId(customer_id).all(offset=0, count=amount_of_payments_to_retrieve)

        body += '<p>Customer "%s" has %s payments</p>' % (customer['id'], payments['totalCount'])

        if int(payments['totalCount']) > amount_of_payments_to_retrieve:
            body += '<p><b>Note: Only showing first %s payments</b></p>' % amount_of_payments_to_retrieve

        for payment in payments:
            body += "<p>Payment %s (%s) EUR</p>" % (payment['id'], payment['amount'])

        return body

    except Mollie.API.Error as e:
        return 'API call failed: ' + e.message

if __name__ == '__main__':
    print(main())
