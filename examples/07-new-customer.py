# Example: How to create a new customer with the Mollie API.
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
        # See: https://www.mollie.com/nl/docs/reference/customers/create
        #
        customer = mollie_client.customers.create(
            {"name": "Mr. First Customer", "email": "first.customer@example.com", "locale": "nl_NL"}
        )

        return f"Created new customer '{customer.name}' ({customer.email})"

    except Error as err:
        return f"API call failed: {err}"


if __name__ == "__main__":
    print(main())
