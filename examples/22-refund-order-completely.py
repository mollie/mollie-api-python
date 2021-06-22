# Example: Refund all eligible items for an order using the Mollie API.
#

import os

from mollie.api.client import Client
from mollie.api.error import Error


def main():
    try:
        #
        # Initialize the Mollie API library with your API key.
        #
        #
        api_key = os.environ.get("MOLLIE_API_KEY", "test_test")
        mollie_client = Client()
        mollie_client.set_api_key(api_key)

        #
        #  Refund all eligible items for your first order
        #
        # See: https://docs.mollie.com/reference/v2/orders-api/create-order-refund
        #
        body = "<p>Attempting to retrieve the first page of orders, and grabbing the first.</p>"

        order = next(mollie_client.orders.list())
        refund = order.create_refund()

        body += f"Refund {refund.id} was created for order {order.id}:"

        return body
    except Error as err:
        return f"API call failed: {err}"


if __name__ == "__main__":
    print(main())
