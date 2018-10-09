from mollie.api.objects.order import Order
from mollie.api.objects.order_line import OrderLine
from mollie.api.objects.shipment import Shipment

from .utils import assert_list_object

ORDER_ID = 'ord_kEn1PlbGa'
SHIPMENT_ID = 'shp_3wmsgCJN4U'


def test_get_shipment(client, response):
    """Retrieve a single shipment by a shipment's ID."""
    response.get('https://api.mollie.com/v2/orders/{order_id}'.format(order_id=ORDER_ID), 'order_single')
    response.get('https://api.mollie.com/v2/orders/{order_id}/shipments/{shipment_id}'.format(
        order_id=ORDER_ID, shipment_id=SHIPMENT_ID), 'shipment_single')

    order = client.orders.get(ORDER_ID)
    shipment = order.get_shipment(SHIPMENT_ID)
    assert isinstance(shipment, Shipment)
    assert shipment.resource == 'shipment'
    assert shipment.id == SHIPMENT_ID
    assert shipment.order_id == ORDER_ID
    assert shipment.created_at == '2018-08-09T14:33:54+00:00'
    assert shipment.tracking == {
        'carrier': 'PostNL',
        'code': '3SKABA000000000',
        'url': 'http://postnl.nl/tracktrace/?B=3SKABA000000000&P=1016EE&D=NL&T=C'
    }
    assert shipment.has_tracking() is True
    assert shipment.has_tracking_url() is True
    assert shipment.tracking_url == 'http://postnl.nl/tracktrace/?B=3SKABA000000000&P=1016EE&D=NL&T=C'
    assert_list_object(shipment.lines, OrderLine)
    assert isinstance(shipment.order, Order)


def test_create_shipment(client, response):
    """Create a shipment of an order object"""
    response.get('https://api.mollie.com/v2/orders/{order_id}'.format(order_id=ORDER_ID), 'order_single')
    response.post('https://api.mollie.com/v2/orders/ord_kEn1PlbGa/shipments', 'shipment_single')

    data = {
        'lines': [
            {
                'id': 'odl_dgtxyl',
                'quantity': 1
            },
            {
                'id': 'odl_dgtxyb'
            }
        ],
        'tracking': {
            'carrier': 'PostNL',
            'code': '3SKABA000000000',
            'url': 'http://postnl.nl/tracktrace/?B=3SKABA000000000&P=1016EE&D=NL&T=C'
        },
    }
    order = client.orders.get(ORDER_ID)
    new_shipment = order.create_shipment(data)
    assert isinstance(new_shipment, Shipment)


def test_update_shipment(client, response):
    """Update the tracking information of a shipment"""
    response.get('https://api.mollie.com/v2/orders/{order_id}'.format(order_id=ORDER_ID), 'order_single')
    response.patch('https://api.mollie.com/v2/orders/{order_id}/shipments/{shipment_id}'.format(
        order_id=ORDER_ID, shipment_id=SHIPMENT_ID), 'shipment_single')

    order = client.orders.get(ORDER_ID)
    data = {
         'tracking': {
             'carrier': 'PostNL',
             'code': '3SKABA000000000',
             'url': 'http://postnl.nl/tracktrace/?B=3SKABA000000000&P=1016EE&D=NL&T=C'
         },
     }
    updated_shipment = order.update_shipment(SHIPMENT_ID, data)
    assert isinstance(updated_shipment, Shipment)
    assert updated_shipment.id == SHIPMENT_ID
