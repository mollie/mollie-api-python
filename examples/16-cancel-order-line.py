# Example: Cancel an order line using the Mollie API.
#

import os

from mollie.api.client import Client
from mollie.api.error import Error


def main():
    try:
        #
        # List the most recent orders
        #
        # See: https://docs.mollie.com/reference/v2/orders-api/list-orders
        #
        api_key = os.environ.get("MOLLIE_API_KEY", "test_test")
        mollie_client = Client()
        mollie_client.set_api_key(api_key)

        #
        # Fetch a list of orders and use the first.
        # Cancel the first order line.
        #
        # See: https://docs.mollie.com/reference/v2/orders-api/cancel-order-line
        #
        body = "<p>Attempting to retrieve the first page of orders, and grabbing the first.</p>"
        order = next(mollie_client.orders.list())
        line = next(order.lines)

        if line and line.is_cancelable:
            data = {"lines": [{"id": line.id, "quantity": 1}]}
            order.cancel_lines(data)

            order = mollie_client.orders.get(order.id)
            body += f"Your order {order.id} was updated:"
            for line in order.lines:
                body += f"{line.name} Status: <b>{line.status}</b>"
        else:
            body += f"Unable to cancel line {line.id} for your order {order.id}"
        return body

    except Error as err:
        return f"API call failed: {err}"


if __name__ == "__main__":
    print(main())
