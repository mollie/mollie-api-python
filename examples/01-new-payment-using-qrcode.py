# Example: How to prepare a new payment with the Mollie API, and render the QRcode.
#

import os
import time

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
        # Generate a unique webshop order id for this example. It is important to include this unique attribute
        # in the redirectUrl (below) so a proper return page can be shown to the customer.
        #
        my_webshop_id = int(time.time())

        #
        # Payment parameters:
        # amount        Currency and value. This example creates a € 120,- payment.
        # description   Description of the payment.
        # webhookUrl    Webhook location, used to report when the payment changes state.
        # redirectUrl   Redirect location. The customer will be redirected there after the payment.
        # metadata      Custom metadata that is stored with the payment.
        #
        # include=...   Request an optional QRcode from Mollie.
        #
        payment = mollie_client.payments.create(
            {
                "amount": {"currency": "EUR", "value": "120.00"},
                "description": "My first API payment",
                "webhookUrl": f"{PUBLIC_URL}02-webhook-verification",
                "redirectUrl": f"{PUBLIC_URL}03-return-page?my_webshop_id={my_webshop_id}",
                "metadata": {"my_webshop_id": str(my_webshop_id)},
            },
            include="details.qrCode",
        )

        #
        # In this example we store the order with its payment status in a database.
        #
        data = {"status": payment.status}
        database_write(my_webshop_id, data)

        #
        # Display the QRcode to the customer, to complete the payment.
        #
        qr_code = payment.details["qrCode"]
        body = f"""
        Use the QRcode or visit the checkout page to complete the payment.
        <hr/>
        <img src='{qr_code["src"]}' />
        <hr/>
        <a href="{payment.checkout_url}">Visit checkout page</a>.
        """

        return body

    except Error as err:
        return f"API call failed: {err}"


if __name__ == "__main__":
    print(main())
