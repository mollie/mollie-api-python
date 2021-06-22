# Example: Handle an order status change using the Mollie API.
#

import os

import flask

from app import database_write
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
        # After your webhook has been called with the order ID in its body, you'd like
        # to handle the order's status change. This is how you can do that.
        #
        # See: https://docs.mollie.com/reference/v2/orders-api/get-order
        #
        if "id" not in flask.request.form:
            flask.abort(404, "Unknown order id")

        order_id = flask.request.form["id"]
        order = mollie_client.orders.get(order_id)
        my_webshop_id = order.metadata["my_webshop_id"]
        #
        # Update the order in the database.
        #
        data = {"order_id": order.id, "status": order.status}
        database_write(my_webshop_id, data)

        if order.is_paid() or order.is_authorized():
            #
            # At this point you'd probably want to start the process of delivering the product to the customer.
            #
            return "Paid"
        if order.is_canceled():
            #
            # At this point you'd probably want to inform the customer that the order has been canceled.
            #
            return "Canceled"
        if order.is_completed():
            #
            # At this point you could inform the customer that all deliveries to the customer have started.
            #
            return "Completed"

    except Error as err:
        return f"API call failed: {err}"


if __name__ == "__main__":
    print(main())
