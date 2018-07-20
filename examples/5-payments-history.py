# coding=utf-8
#
# Example 5 - How to retrieve your payments history.
#
from __future__ import print_function

import os

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

        #
        # Get the all payments for this API key ordered by newest.
        #
        payments = mollie_client.payments.all()

        body = 'Your API key has %u payments, last %u:<br>' % (payments['totalCount'], payments['count'])

        for payment in payments:
            body += "&euro; %s, status: '%s'<br>" % (payment['amount'], payment['status'])

        return body

    except mollie.api.error as e:
        return 'API call failed: ' + str(e)

if __name__ == '__main__':
    print(main())
