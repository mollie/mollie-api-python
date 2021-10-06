#
# Example: How to show a return page to the customer.
#
# In this example we retrieve the order stored in the database.
#

import os

import flask

from app import database_read
from mollie.api.client import Client


def main():
    api_key = os.environ.get("MOLLIE_API_KEY", "test_test")
    mollie_client = Client()
    mollie_client.set_api_key(api_key)

    if "my_webshop_id" not in flask.request.args:
        flask.abort(404, "Unknown webshop id")

    data = database_read(flask.request.args["my_webshop_id"])

    order = mollie_client.orders.get(data["order_id"])

    if order.is_paid():
        return f"The payment for your order {order.id} has been processed"

    elif order.is_canceled():
        return f"Your order {order.id} has been canceled"

    elif order.is_shipping():
        return f"Your order {order.id} is shipping"

    elif order.is_created():
        return f"Your order {order.id} has been created"

    elif order.is_authorized():
        return f"Your order {order.id} is authorized"

    elif order.is_refunded():
        return f"Your order {order.id} has been refunded"

    elif order.is_expired():
        return f"Your order {order.id} has expired"

    elif order.is_completed():
        return f"Your order {order.id} is completed"

    else:
        return f"The status of your order {order.id} is: {order.status}"


if __name__ == "__main__":
    print(main())
