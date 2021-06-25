# Example: Update shipment tracking information using the Mollie API.
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
        #  Update the tracking information for a shipment
        #
        # See: https://docs.mollie.com/reference/v2/shipments-api/update-shipment
        #
        body = "<p>Attempting to retrieve the first page of orders, and grabbing the first.</p>"
        order = next(mollie_client.orders.list())

        if not len(order.shipments):
            body += "<p>You have no shipments. You can create one from the examples.</p>"
            return body

        body = "<p>Attempting to retrieve the first page of shipments if your order, and grabbing the first.</p>"
        shipment = next(order.shipments)

        tracking = {
            "carrier": "PostNL",
            "code": "3SKABA000000000",
            "url": "http://postnl.nl/tracktrace/?B=3SKABA000000000&P=1016EE&D=NL&T=C",
        }
        shipment = order.update_shipment(shipment.id, tracking)

        body += f"Shipment {shipment.id} for order {order.id}:"
        body += "Tracking information updated:"
        body += f'Carrier: {shipment.tracking["carrier"]}'
        body += f'Code: {shipment.tracking["code"]}'
        body += f"Url: {shipment.tracking_url}"

        for line in shipment.lines:
            body += f"{line.name} Status: <b>{line.status}</b>"

        return body
    except Error as err:
        return f"API call failed: {err}"


if __name__ == "__main__":
    print(main())
