# coding=utf-8
#
# Example 7 - How to create a new customer with the Mollie API.
#
from __future__ import print_function

import sys, os

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

        #
        # See: https://www.mollie.com/nl/docs/reference/customers/create
        #
        customer = mollie.customers.create({
            'name': 'Mr. First Customer',
            'email': 'first.customer@example.com',
            'locale': 'nl_NL'
        })

        return "Created new customer '%s' (%s)" % (customer['name'], customer['email'])

    except Mollie.API.Error as e:
        return 'API call failed: ' + e.message


if __name__ == '__main__':
    print(main())
