import json

import pytest

from mollie.api.error import DataConsistencyError
from mollie.api.objects.order_line import OrderLine

from .utils import assert_list_object

ORDER_ID = "ord_kEn1PlbGa"
LINE_ID = "odl_dgtxyl"


def test_get_order_lines(client, response):
    """Retrieve lines of a single order by order ID."""
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_single")

    order = client.orders.get(ORDER_ID)
    lines = order.lines.list()
    assert_list_object(lines, OrderLine)

    # Test properties of the first line
    line = next(lines)
    assert isinstance(line, OrderLine)
    assert line.id == LINE_ID
    assert line.resource == "orderline"
    assert line.order_id == ORDER_ID
    assert line.type == "physical"
    assert line.name == "LEGO 42083 Bugatti Chiron"
    assert line.status == "created"
    assert line.is_cancelable is True
    assert line.quantity == 2
    assert line.shippable_quantity == 0
    assert line.quantity_shipped == 0
    assert line.amount_shipped == {"value": "0.00", "currency": "EUR"}
    assert line.refundable_quantity == 0
    assert line.quantity_refunded == 0
    assert line.amount_refunded == {"value": "0.00", "currency": "EUR"}
    assert line.cancelable_quantity == 0
    assert line.quantity_canceled == 0
    assert line.amount_canceled == {"value": "0.00", "currency": "EUR"}
    assert line.unit_price == {"value": "399.00", "currency": "EUR"}
    assert line.discount_amount == {"value": "100.00", "currency": "EUR"}
    assert line.total_amount == {"value": "698.00", "currency": "EUR"}
    assert line.vat_rate == "21.00"
    assert line.vat_amount == {"value": "121.14", "currency": "EUR"}
    assert line.sku == "5702016116977"
    assert line.image_url == "https://sh-s7-live-s.legocdn.com/is/image//LEGO/42083_alt1?$main$"
    assert line.product_url == "https://shop.lego.com/nl-NL/Bugatti-Chiron-42083"
    assert line.created_at == "2018-08-02T09:29:56+00:00"
    assert line.metadata == {"brickwatch_url": "https://www.brickwatch.net/nl-NL/set/42083/Bugatti-Chiron.html"}
    assert line.is_created() is True
    assert line.is_authorized() is False
    assert line.is_paid() is False
    assert line.is_shipping() is False
    assert line.is_canceled() is False
    assert line.is_completed() is False


def test_update_order_line(client, response):
    """Update a line by id through an order object."""
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_single")
    response.patch(f"https://api.mollie.com/v2/orders/{ORDER_ID}/lines/{LINE_ID}", "order_single")
    data = {
        "name": "LEGO 71043 Hogwarts Castle",
        "productUrl": "https://shop.lego.com/en-GB/product/Hogwarts-Castle-71043",
        "imageUrl": "https://sh-s7-live-s.legocdn.com/is/image//LEGO/71043_alt1?$main$",
        "quantity": 2,
        "sku": "335596985",
        "vatRate": "21.00",
        "unitPrice": {"currency": "EUR", "value": "349.00"},
        "totalAmount": {"currency": "EUR", "value": "598.00"},
        "discountAmount": {"currency": "EUR", "value": "100.00"},
        "vatAmount": {"currency": "EUR", "value": "103.79"},
    }
    order = client.orders.get(ORDER_ID)
    update = order.lines.update(LINE_ID, data)
    assert isinstance(update, OrderLine)

    # Inspect the request that was sent
    request = response.calls[-1].request
    assert request.url == f"https://api.mollie.com/v2/orders/{ORDER_ID}/lines/{LINE_ID}"
    assert json.loads(request.body) == data


def test_update_order_line_unexpected_response_raises_data_consistency_error(client, response):
    """When the API sends us data we did not expect raise an consistency error.

    This test is a bit tricky, since we send an orderline_id that is not in the order. Normally
    it is expected that the API would give us an error because of that, but we ignore that fact
    for the sake of the test: we want the API to return us data that simply doesn't match the request.
    """
    OTHER_LINE_ID = "odl_kekjo"
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_single")
    response.patch(f"https://api.mollie.com/v2/orders/{ORDER_ID}/lines/{OTHER_LINE_ID}", "order_single")

    order = client.orders.get(ORDER_ID)
    data = {
        "name": "LEGO 71043 Hogwarts™ Castle",
    }

    # Update an nonexistent order line. This raises an data consistency error.
    with pytest.raises(DataConsistencyError) as excinfo:
        order.lines.update(OTHER_LINE_ID, data)
    assert str(excinfo.value) == "OrderLine with id 'odl_kekjo' not found in response."


def test_cancel_order_lines(client, response):
    """Cancel a line of an order."""
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_single")
    response.delete(f"https://api.mollie.com/v2/orders/{ORDER_ID}/lines", "empty", 204)

    order = client.orders.get(ORDER_ID)
    line = next(order.lines.list())
    data = {
        "lines": [
            {"id": line.id, "quantity": line.quantity},
        ]
    }
    order.lines.delete_lines(data)

    # Inspect the request that was sent
    request = response.calls[-1].request
    assert request.url == f"https://api.mollie.com/v2/orders/{ORDER_ID}/lines"
    assert json.loads(request.body) == data


def test_cancel_order_lines_all(client, response):
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_single")
    response.delete(f"https://api.mollie.com/v2/orders/{ORDER_ID}/lines", "empty", 204)

    order = client.orders.get(ORDER_ID)
    order.lines.delete_lines()

    # Inspect the request that was sent
    request = response.calls[-1].request
    assert request.url == f"https://api.mollie.com/v2/orders/{ORDER_ID}/lines"
    assert json.loads(request.body) == {
        "lines": []
    }, "An empty list of lines should be generated, so all lines will be cancelled."


def test_cancel_single_order_line(client, response):
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_single")
    response.delete(f"https://api.mollie.com/v2/orders/{ORDER_ID}/lines", "empty", 204)

    order = client.orders.get(ORDER_ID)
    order.lines.delete(LINE_ID)

    # Inspect the request that was sent
    request = response.calls[-1].request
    assert request.url == f"https://api.mollie.com/v2/orders/{ORDER_ID}/lines"
    assert json.loads(request.body) == {
        "lines": [
            {
                "id": LINE_ID,
            }
        ]
    }, "The correct payload for deleting a single line should be generated."
