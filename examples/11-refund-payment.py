# coding=utf-8
#
# Example 11 - How to prepare a new refund with the Mollie API.
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

        payments = mollie_client.payments.all()

        body += '<p>Attempting to retrieve all payments and grabbing the first.</p>'

        if int(payments.count) == 0:
            body += '<p>You have no payments. You can create one from the examples.</p>'
            return body

        for payment in payments:
            payment_id = payment.id
            break

        payment = mollie_client.payments.get(payment_id)
        if payment.can_be_refunded and payment.amount_remaining['currency'] == 'EUR' \
                and float(payment.amount_remaining['value']) >= 2.0:
            data = {
                'amount': {'value': '2.00', 'currency': 'EUR'}
            }
            refund = mollie_client.payment_refunds.with_parent_id(payment_id).create(data)
            body += '<p>%s %s of payment %s refunded</p>' % (refund.amount['currency'], refund.amount['value'],
                                                             payment_id)
        else:
            body += '<p>Payment %s can not be refunded</p>' % payment_id
        return body
    except Error as err:
        return 'API call failed: %s' % err


if __name__ == '__main__':
    print(main())
