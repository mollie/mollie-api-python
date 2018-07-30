# coding=utf-8
#
# Example 7 - How to create a new customer with the Mollie API.
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
        mollie_client.set_api_key(api_key)

        #
        # See: https://www.mollie.com/nl/docs/reference/customers/create
        #
        customer = mollie_client.customers.create({
            'name': 'Mr. First Customer',
            'email': 'first.customer@example.com',
            'locale': 'nl_NL'
        })

        return "Created new customer '%s' (%s)" % (customer.name, customer.email)

    except mollie.api.error as e:
        return 'API call failed: ' + str(e)


if __name__ == '__main__':
    print(main())
