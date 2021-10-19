#  Example: How to get the currently activated payment methods.
#

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
        api_key = os.environ.get("MOLLIE_API_KEY", "test_test")
        mollie_client = Client()
        mollie_client.set_api_key(api_key)

        #
        # Get the all the activated methods for this API key.
        #
        params = {
            "amount": {
                "currency": "EUR",
                "value": "100.00",
            }
        }
        methods = mollie_client.methods.list(**params)
        body = f"Your API key has {len(methods)} activated payment methods:<br>"

        for method in methods:
            body += '<div style="line-height:40px; vertical-align:top">'
            body += f'<img src="{method.image_svg}"> {method.description} ({method.id})'
            body += "</div>"

        return body

    except Error as err:
        return f"API call failed: {err}"


if __name__ == "__main__":
    print(main())
