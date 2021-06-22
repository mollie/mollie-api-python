# Example: How to retrieve your payments history.
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
        # Get the first page of payments for this API key ordered by newest.
        #
        payments = mollie_client.payments.list()

        body = ""

        if not len(payments):
            body += "<p>You have no payments. You can create one from the examples.</p>"
            return body

        body += "<p>Showing the first page of payments for this API key</p>"

        for payment in payments:
            body += f'{payment.amount["currency"]} {payment.amount["value"]}, status: \'{payment.status}\'<br>'
        return body

    except Error as err:
        return f"API call failed: {err}"


if __name__ == "__main__":
    print(main())
