# coding=utf-8
#
# Example 5 - How to retrieve your payments history.
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

        #
        # Get the all payments for this API key ordered by newest.
        #
        payments = mollie_client.payments.all()

        body = 'Your API key has %u payments<br>' % payments.count

        for payment in payments:
            body += "%s %s, status: '%s'<br>" % (payment.amount['value'], payment.amount['currency'], payment.status)

        return body

    except Error as err:
        return 'API call failed: ' + str(err)


if __name__ == '__main__':
    print(main())
