#  Example: Retrieving the payment history for a customer
#

import os

import flask

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

        body = ""

        customer_id = flask.request.args.get("customer_id")

        # If no customer ID was provided in the URL, we grab the first customer
        if customer_id is None:
            customers = mollie_client.customers.list()

            body += "<p>No customer ID specified. Attempting to retrieve the first page of customers "
            body += "and grabbing the first.</p>"

            if not len(customers):
                body += "<p>You have no customers. You can create one from the examples.</p>"
                return body

            customer = next(customers)
        else:
            customer = mollie_client.customers.get(customer_id)

        amount_of_payments_to_retrieve = 20

        #
        # Retrieve the latest payments for the customer
        #
        # See: https://www.mollie.com/nl/docs/reference/customers/list-payments
        #
        params = {
            "limit": amount_of_payments_to_retrieve,
        }
        payments = mollie_client.customer_payments.with_parent_id(customer.id).list(**params)

        body += f'<p>Showing the last {len(payments)} payments for customer "{customer.id}"</p>'

        for payment in payments:
            body += f'<p>Payment {payment.id} ({payment.amount["value"]}) {payment.amount["currency"]}</p>'
        return body

    except Error as err:
        return f"API call failed: {err}"


if __name__ == "__main__":
    print(main())
