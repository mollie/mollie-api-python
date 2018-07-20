# coding=utf-8
#
#  Example 6 - How to get the currently activated payment methods.
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
        # Get the all the activated methods for this API key.
        #
        params = {
            'amount': {
                'currency': 'EUR',
                'value': '100.00',
            }
        }
        methods = mollie_client.methods.all(**params)
        body = 'Your API key has %u activated payment methods:<br>' % methods.count

        for method in methods:
            body += '<div style="line-height:40px; vertical-align:top">'
            body += '<img src="%s"> %s (%s)' % (method.image_size2x, method.description, method.id)
            body += '</div>'

        return body

    except mollie.api.error as e:
        return 'API call failed: ' + str(e)


if __name__ == '__main__':
    print(main())
