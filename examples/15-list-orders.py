# Example: List orders using the Mollie API.
#

import os

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
        # List the most recent orders
        #
        # See: https://docs.mollie.com/reference/v2/orders-api/list-orders
        #
        body = ""
        orders = mollie_client.orders.list()
        if not len(orders):
            body += "<p>You have no orders. You can create one from the examples.</p>"
            return body

        body += f"<p>Showing the last {len(orders)} orders for your API key.</p>"

        body += """
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Billed to</th>
                        <th>Shipped to</th>
                        <th>Total amount</th>
                    </tr>
                </thead>
                <tbody>
        """

        for order in orders:
            body += "<tr>"
            body += f"<td>{order.id}</td>"
            body += f'<td>{order.billing_address["givenName"]} {order.billing_address["familyName"]}</td>'
            body += f'<td>{order.shipping_address["givenName"]} {order.shipping_address["familyName"]}</td>'
            body += f'<td>{order.amount["currency"]} {order.amount["value"]}</td>'
            body += f'<td><a href="{order.checkout_url}" target="_blank">Pay order</a></td>'
            body += f'<td><a href="/14-cancel-order?order_id={order.id}">Cancel order</a></td>'
            body += f'<td><a href="/18-ship-order-completely?order_id={order.id}">Ship order</a></td>'
            body += "</tr>"

        body += "</tbody></table>"
        return body

    except Error as err:
        return f"API call failed: {err}"


if __name__ == "__main__":
    print(main())
