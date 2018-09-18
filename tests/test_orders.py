from mollie.api.objects.order import Order
from mollie.api.objects.refund import Refund

from .utils import assert_list_object

ORDER_ID = 'ord_kEn1PlbGa'


def test_get_order(client, response):
    """Retrieve a single order by order ID"""
    response.get('https://api.mollie.com/v2/orders/{order_id}'.format(order_id=ORDER_ID), 'order_single')

    order = client.orders.get(ORDER_ID)
    assert isinstance(order, Order)
    assert order.id == 'ord_kEn1PlbGa'
    assert order.profile_id == 'pfl_URR55HPMGx'
    assert order.method == 'ideal'
    assert order.amount == {'value': '1027.99', 'currency': 'EUR'}
    assert order.amount_captured == {'value': '0.00', 'currency': 'EUR'}
    assert order.amount_refunded == {'value': '0.00', 'currency': 'EUR'}
    assert order.status == 'created'
    assert order.is_created
    assert order.is_cancelable
    assert order.metadata is None
    assert order.created_at == '2018-08-02T09:29:56+00:00'
    assert order.expires_at == '2018-08-30T09:29:56+00:00'
    assert order.mode == 'live'
    assert order.locale == 'nl_NL'
    assert order.order_number == '18475'
    assert order.billing_address == {
        'streetAndNumber': 'Keizersgracht 313',
        'postalCode': '1016 EE',
        'city': 'Amsterdam',
        'country': 'nl',
        'givenName': 'Luke',
        'familyName': 'Skywalker',
        'email': 'luke@skywalker.com'
    }
    assert order.shipping_address == {
        'streetAndNumber': 'Keizersgracht 313',
        'postalCode': '1016 EE',
        'city': 'Amsterdam',
        'country': 'nl',
        'givenName': 'Luke',
        'familyName': 'Skywalker',
        'email': 'luke@skywalker.com'
    }
    assert order.checkout_url == 'https://www.mollie.com/payscreen/order/checkout/pbjz8x'


def test_list_orders(client, response):
    """Retrieve a list of existing orders."""
    response.get('https://api.mollie.com/v2/orders', 'orders_list')

    orders = client.orders.list()
    assert_list_object(orders, Order)


def test_create_order_refund(client, response):
    """Create an order refund of an order."""

    response.get('https://api.mollie.com/v2/orders/{order_id}'.format(order_id=ORDER_ID), 'order_single')
    response.post('https://api.mollie.com/v2/orders/{order_id}/refunds'.format(order_id=ORDER_ID), 'refund_single')

    data = {
        "lines": [
            {
                "id": "odl_dgtxyl",
                "quantity": 1
            }
        ],
        "description": "Required quantity not in stock, refunding one photo book."
    }

    order = client.orders.get(ORDER_ID)
    refund = order.create_refund(data)
    assert isinstance(refund, Refund)
