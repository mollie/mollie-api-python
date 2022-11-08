import json

import pytest

from mollie.api.error import IdentifierError
from mollie.api.objects.order import Order
from mollie.api.objects.order_line import OrderLine
from mollie.api.objects.shipment import Shipment

from .utils import assert_list_object

ORDER_ID = "ord_kEn1PlbGa"
SHIPMENT_ID = "shp_3wmsgCJN4U"


def test_get_shipment(client, response):
    """Retrieve a single shipment by a shipment's ID."""
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_single")
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}/shipments/{SHIPMENT_ID}", "shipment_single")

    order = client.orders.get(ORDER_ID)
    shipment = order.shipments.get(SHIPMENT_ID)
    assert isinstance(shipment, Shipment)
    assert shipment.resource == "shipment"
    assert shipment.id == SHIPMENT_ID
    assert shipment.order_id == ORDER_ID
    assert shipment.created_at == "2018-08-09T14:33:54+00:00"
    assert shipment.tracking == {
        "carrier": "PostNL",
        "code": "3SKABA000000000",
        "url": "http://postnl.nl/tracktrace/?B=3SKABA000000000&P=1016EE&D=NL&T=C",
    }
    assert shipment.has_tracking() is True
    assert shipment.has_tracking_url() is True
    assert shipment.tracking_url == "http://postnl.nl/tracktrace/?B=3SKABA000000000&P=1016EE&D=NL&T=C"
    assert_list_object(shipment.lines, OrderLine)


def test_create_shipment(client, response):
    """Create a shipment of an order object"""
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_single")
    response.post(f"https://api.mollie.com/v2/orders/{ORDER_ID}/shipments", "shipment_single")

    data = {
        "lines": [{"id": "odl_dgtxyl", "quantity": 1}, {"id": "odl_dgtxyb"}],
        "tracking": {
            "carrier": "PostNL",
            "code": "3SKABA000000000",
            "url": "http://postnl.nl/tracktrace/?B=3SKABA000000000&P=1016EE&D=NL&T=C",
        },
    }
    order = client.orders.get(ORDER_ID)
    new_shipment = order.shipments.create(data)
    assert isinstance(new_shipment, Shipment)


def test_create_shipment_all_lines(client, response):
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_single")
    response.post(f"https://api.mollie.com/v2/orders/{ORDER_ID}/shipments", "shipment_single")

    order = client.orders.get(ORDER_ID)
    new_shipment = order.shipments.create()
    assert isinstance(new_shipment, Shipment)

    # Inspect the request that was made
    request = response.calls[-1].request
    assert request.url == f"https://api.mollie.com/v2/orders/{ORDER_ID}/shipments"
    assert json.loads(request.body) == {
        "lines": []
    }, "An empty list of lines should be generated, so all lines will be shipped."


def test_update_shipment(client, response):
    """Update the tracking information of a shipment"""
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_single")
    response.patch(f"https://api.mollie.com/v2/orders/{ORDER_ID}/shipments/{SHIPMENT_ID}", "shipment_single")

    order = client.orders.get(ORDER_ID)
    data = {
        "tracking": {
            "carrier": "PostNL",
            "code": "3SKABA000000000",
            "url": "http://postnl.nl/tracktrace/?B=3SKABA000000000&P=1016EE&D=NL&T=C",
        },
    }
    updated_shipment = order.shipments.update(SHIPMENT_ID, data)
    assert isinstance(updated_shipment, Shipment)
    assert updated_shipment.id == SHIPMENT_ID


def test_get_shipment_invalid_id(client, response):
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_single")

    order = client.orders.get(ORDER_ID)

    with pytest.raises(IdentifierError) as excinfo:
        order.shipments.get("invalid")
    assert str(excinfo.value) == "Invalid shipment ID 'invalid', it should start with 'shp_'."


def test_update_shipment_invalid_id(client, response):
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_single")

    order = client.orders.get(ORDER_ID)
    data = {}
    with pytest.raises(IdentifierError) as excinfo:
        order.shipments.update("invalid", data)
    assert str(excinfo.value) == "Invalid shipment ID 'invalid', it should start with 'shp_'."


def test_shipment_get_related_order(client, response):
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}", "order_single")
    response.get(f"https://api.mollie.com/v2/orders/{ORDER_ID}/shipments/{SHIPMENT_ID}", "shipment_single")

    order = client.orders.get(ORDER_ID)
    shipment = order.shipments.get(SHIPMENT_ID)
    related_order = shipment.get_order()
    assert isinstance(related_order, Order)
    assert related_order.id == related_order.id
