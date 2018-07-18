# coding=utf-8
#
#  Example 6 - How to get the currently activated payment methods.
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
        # Get the all the activated methods for this API key.
        #
        params = {
            'amount': {
                'currency': 'EUR',
                'value': '100.00',
            }
        }
        methods = mollie.methods.all(**params)
        body = 'Your API key has %u activated payment methods:<br>' % methods.count

        for method in methods:
            body += '<div style="line-height:40px; vertical-align:top">'
            body += '<img src="%s"> %s (%s)' % (method.image_size2x, method.description, method.id)
            body += '</div>'

        return body

    except Mollie.API.Error as e:
        return 'API call failed: ' + str(e)

if __name__ == '__main__':
    print(main())
