# coding=utf-8
#
#  Example 9 - Creating a payment for a customer
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

        #
        # Generate a unique order number for this example. It is important to include this unique attribute
        # in the redirectUrl (below) so a proper return page can be shown to the customer.
        #
        order_nr = int(time.time())

        #
        # See: https://www.mollie.com/nl/docs/reference/customers/create-payment
        #
        payment = mollie.customer_payments.withParentId(customer_id).create({
            'amount':      (time.time() % 15) * 3,  # Create some variety in the payment amounts
            'description': 'My first API payment',
            'webhookUrl':  flask.request.url_root + '2-webhook-verification?order_nr=' + str(order_nr),
            'redirectUrl': flask.request.url_root + '3-return-page?order_nr=' + str(order_nr),
            'metadata':    {
                'order_nr': order_nr
            }
        })

        database_write(order_nr, payment['status'])

        return '<p>Created payment of %s EUR for %s (%s)<p>' % (payment['amount'], customer['name'], customer['id'])

    except Mollie.API.Error as e:
        return 'API call failed: ' + str(e)

if __name__ == '__main__':
    print(main())
