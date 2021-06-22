# Example: Retrieve a list of shipments using the Mollie API.
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
        # Listing shipments for the first order.
        #
        # See: https://docs.mollie.com/reference/v2/shipments-api/list-shipments
        #
        body = "<p>Attempting to retrieve the first page of orders, and grabbing the first.</p>"
        order = next(mollie_client.orders.list())
        shipments = order.shipments

        body += f"Shipments for order with ID {order.id}:"
        body += """
            <table>
                <thead>
                    <tr>
                        <th>Shipment ID</th>
                        <th>Tracking url</th>
                        <th>Created at</th>
                    </tr>
                </thead>
                <tbody>
        """
        for shipment in shipments:
            body += "<tr>"
            body += f"<td>{shipment.id}</td>"
            body += f"<td>{shipment.tracking_url}</td>"
            body += f"<td>{shipment.created_at}</td>"
            body += "</tr>"

        body += "</tbody></table>"

        return body
    except Error as err:
        return f"API call failed: {err}"


if __name__ == "__main__":
    print(main())
