# coding=utf-8
#
# Example: How to prepare a new refund with the Mollie API.
#
from __future__ import print_function

import os

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
        payment_id = ''

        body += '<p>Attempting to retrieve the first page of payments and grabbing the first.</p>'

        payments = mollie_client.payments.list()

        if not len(payments):
            body += '<p>You have no payments. You can create one from the examples.</p>'
            return body

        payment = next(payments)

        if payment.can_be_refunded() and payment.amount_remaining['currency'] == 'EUR' \
                and float(payment.amount_remaining['value']) >= 2.0:
            data = {
                'amount': {'value': '2.00', 'currency': 'EUR'}
            }
            refund = mollie_client.payment_refunds.with_parent_id(payment_id).create(data)
            body += '<p>{curr} {value} of payment {id} refunded</p>'.format(
                curr=refund.amount['currency'], value=refund.amount['value'], id=payment_id)
        else:
            body += '<p>Payment {id} can not be refunded</p>'.format(id=payment_id)
        return body
    except Error as err:
        return 'API call failed: {error}'.format(error=err)


if __name__ == '__main__':
    print(main())
