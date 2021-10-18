#  Example: Creating a payment for a customer
#

import os
import time

import flask

from app import database_write, get_public_url
from mollie.api.client import Client
from mollie.api.error import Error

PUBLIC_URL = get_public_url()


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

        body = ""

        customer_id = flask.request.args.get("customer_id")

        # If no customer ID was provided in the URL, we grab the first customer
        if customer_id is None:
            customers = mollie_client.customers.list()

            body += "<p>No customer ID specified. Attempting to retrieve the first page of "
            body += "customers and grabbing the first.</p>"

            if not len(customers):
                body += "<p>You have no customers. You can create one from the examples.</p>"
                return body

            customer = next(customers)
        else:
            customer = mollie_client.customers.get(customer_id)

        #
        # Generate a unique webshop order number for this example. It is important to include this unique attribute
        # in the redirectUrl (below) so a proper return page can be shown to the customer.
        #
        my_webshop_id = int(time.time())

        #
        # See: https://www.mollie.com/nl/docs/reference/customers/create-payment
        #
        payment = mollie_client.customer_payments.with_parent_id(customer.id).create(
            {
                "amount": {"currency": "EUR", "value": "100.00"},
                "description": "My first API payment",
                "webhookUrl": f"{PUBLIC_URL}02-webhook-verification",
                "redirectUrl": f"{PUBLIC_URL}03-return-page?my_webshop_id={my_webshop_id}",
                "metadata": {"my_webshop_id": str(my_webshop_id)},
            }
        )
        data = {"status": payment.status}
        database_write(my_webshop_id, data)

        return (
            f'<p>Created payment of {payment.amount["currency"]} {payment.amount["value"]} '
            f"for {customer.name} ({customer.id})<p>"
        )
    except Error as err:
        return f"API call failed: {err}"


if __name__ == "__main__":
    print(main())
