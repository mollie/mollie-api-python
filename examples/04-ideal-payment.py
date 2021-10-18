# Example: How to prepare an iDEAL payment with the Mollie API.
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

        #
        # First, let the customer pick the bank in a simple HTML form. This step is actually optional.
        #
        if "issuer" not in flask.request.form:
            body = '<form method="post">Select your bank: <select name="issuer">'
            for issuer in mollie_client.methods.get("ideal", include="issuers").issuers:
                body += f'<option value="{issuer.id}">{issuer.name}</option>'
            body += '<option value="">or select later</option>'
            body += "</select><button>OK</button></form>"
            return body

        else:
            #
            # Get the posted issuer id.
            #
            issuer_id = None

            if flask.request.form["issuer"]:
                issuer_id = str(flask.request.form["issuer"])

        #
        # Generate a unique webshop order id for this example. It is important to include this unique attribute
        # in the redirectUrl (below) so a proper return page can be shown to the customer.
        #
        my_webshop_id = int(time.time())

        #
        # Payment parameters:
        # amount        Currency and value. This example creates a € 10,- payment.
        # description   Description of the payment.
        # webhookUrl    Webhook location, used to report when the payment changes state.
        # redirectUrl   Redirect location. The customer will be redirected there after the payment.
        # metadata      Custom metadata that is stored with the payment.
        # method        Payment method "ideal".
        # issuer        The customer's bank. If empty the customer can select it later.
        #
        payment = mollie_client.payments.create(
            {
                "amount": {"currency": "EUR", "value": "10.00"},
                "description": "My first API payment",
                "webhookUrl": f"{PUBLIC_URL}02-webhook-verification",
                "redirectUrl": f"{PUBLIC_URL}03-return-page?my_webshop_id={my_webshop_id}",
                "metadata": {
                    "my_webshop_id": str(my_webshop_id),
                },
                "method": "ideal",
                "issuer": issuer_id,
            }
        )

        #
        # In this example we store the order with its payment status in a database.
        #
        data = {"status": payment.status}
        database_write(my_webshop_id, data)

        #
        # Send the customer off to complete the payment.
        #
        return flask.redirect(payment.checkout_url)

    except Error as err:
        return f"API call failed: {err}"


if __name__ == "__main__":
    print(main())
