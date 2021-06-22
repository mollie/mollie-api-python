#
# Example: How to verify Mollie API Payments in a webhook.
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
        # Retrieve the payment's current state.
        #
        if "id" not in flask.request.form:
            flask.abort(404, "Unknown payment id")

        payment_id = flask.request.form["id"]
        payment = mollie_client.payments.get(payment_id)
        my_webshop_id = payment.metadata["my_webshop_id"]

        #
        # Update the order in the database.
        #
        data = {"status": payment.status}
        database_write(my_webshop_id, data)

        if payment.is_paid():
            #
            # At this point you'd probably want to start the process of delivering the product to the customer.
            #
            return "Paid"
        elif payment.is_pending():
            #
            # The payment has started but is not complete yet.
            #
            return "Pending"
        elif payment.is_open():
            #
            # The payment has not started yet. Wait for it.
            #
            return "Open"
        else:
            #
            # The payment isn't paid, pending nor open. We can assume it was aborted.
            #
            return "Cancelled"

    except Error as err:
        return f"API call failed: {err}"


if __name__ == "__main__":
    print(main())
