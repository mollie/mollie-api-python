# coding=utf-8
#
#  Example: How to get the currently activated payment methods.
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
        # Get the all the activated methods for this API key.
        #
        params = {
            'amount': {
                'currency': 'EUR',
                'value': '100.00',
            }
        }
        methods = mollie_client.methods.list(**params)
        body = 'Your API key has {num} activated payment methods:<br>'.format(num=len(methods))

        for method in methods:
            body += '<div style="line-height:40px; vertical-align:top">'
            body += '<img src="{url}"> {desc} ({id})'.format(
                url=method.image_svg, desc=method.description, id=method.id)
            body += '</div>'

        return body

    except Error as err:
        return 'API call failed: {error}'.format(error=err)


if __name__ == '__main__':
    print(main())
