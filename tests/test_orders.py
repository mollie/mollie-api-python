from mollie.api.objects.order import Order
from mollie.api.objects.refund import Refund
from mollie.api.objects.shipment import Shipment

from .utils import assert_list_object

ORDER_ID = 'ord_kEn1PlbGa'


def test_get_order(client, response):
    """Retrieve a single order by order ID."""
    response.get('https://api.mollie.com/v2/orders/{order_id}'.format(order_id=ORDER_ID), 'order_single')
    response.get('https://api.mollie.com/v2/orders/{order_id}/shipments'.format(order_id=ORDER_ID), 'shipments_list')
    response.get('https://api.mollie.com/v2/orders/{order_id}/refunds'.format(order_id=ORDER_ID), 'order_refunds_list')

    order = client.orders.get(ORDER_ID)
    assert isinstance(order, Order)
    assert order.id == 'ord_kEn1PlbGa'
    assert order.resource == 'order'
    assert order.profile_id == 'pfl_URR55HPMGx'
    assert order.method == 'ideal'
    assert order.mode == 'live'
    assert order.amount == {'value': '1027.99', 'currency': 'EUR'}
    assert order.amount_captured is None
    assert order.amount_refunded is None
    assert order.status == 'created'
    assert order.is_cancelable is True
    assert order.billing_address == {
        "streetAndNumber": "Keizersgracht 313",
        "city": "Amsterdam",
        "region": "Noord-Holland",
        "postalCode": "1234AB",
        "country": "NL",
        "title": "Dhr.",
        "givenName": "Piet",
        "familyName": "Mondriaan",
        "email": "piet@mondriaan.com",
        "phone": "+31309202070"
    }
    assert order.consumer_date_of_birth == '1958-01-31'
    assert order.order_number == '1337'
    assert order.shipping_address == {
        'streetAndNumber': 'Keizersgracht 313',
        'streetAdditional': '4th floor',
        'city': 'Haarlem',
        'region': 'Noord-Holland',
        'postalCode': '5678AB',
        'country': 'NL',
        'title': 'Mr.',
        'givenName': 'Chuck',
        'familyName': 'Norris',
        'email': 'norris@chucknorrisfacts.net'
    }
    assert order.locale == 'nl_NL'
    assert order.metadata == {'description': 'Lego cars', 'order_id': '1337'}
    assert order.redirect_url == 'https://example.org/redirect'
    assert order.webhook_url == 'https://example.org/webhook'
    assert order.created_at == '2018-08-02T09:29:56+00:00'
    assert order.expires_at == '2018-08-30T09:29:56+00:00'
    assert order.expired_at is None
    assert order.paid_at is None
    assert order.authorized_at is None
    assert order.canceled_at is None
    assert order.completed_at is None
    assert order.checkout_url == 'https://www.mollie.com/payscreen/order/checkout/pbjz8x'
    assert_list_object(order.shipments, Shipment)
    assert_list_object(order.refunds, Refund)

    assert order.is_created() is True
    assert order.is_paid() is False
    assert order.is_authorized() is False
    assert order.is_shipping() is False
    assert order.is_completed() is False
    assert order.is_expired() is False


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


def test_create_order(client, response):
    """Create an order."""
    response.post('https://api.mollie.com/v2/orders', 'order_single')

    data = {
        'amount': {
            'value': '1027.99',
            'currency': 'EUR'
        },
        'billingAddress': {
            'streetAndNumber': 'Keizersgracht 313',
            'city': 'Amsterdam',
            'region': 'Noord-Holland',
            'postalCode': '1234AB',
            'country': 'NL',
            'givenName': 'Piet',
            'familyName': 'Mondriaan',
            'email': 'piet@mondriaan.com',
        },
        'shippingAddress': {
            'streetAndNumber': 'Prinsengracht 313',
            'city': 'Haarlem',
            'region': 'Noord-Holland',
            'postalCode': '5678AB',
            'country': 'NL',
            'givenName': 'Chuck',
            'familyName': 'Norris',
            'email': 'norris@chucknorrisfacts.net'
        },
        'metadata': {
            'order_id': '1337',
            'description': 'Lego cars'
        },
        'consumerDateOfBirth': '1958-01-31',
        'locale': 'nl_NL',
        'orderNumber': '1337',
        'redirectUrl': 'https://example.org/redirect',
        'webhookUrl': 'https://example.org/webhook',
        'method': 'klarnapaylater',
        'lines': [
            {
                'type': 'physical',
                'sku': '5702016116977',
                'name': 'LEGO 42083 Bugatti Chiron',
                'productUrl': 'https://shop.lego.com/nl-NL/Bugatti-Chiron-42083',
                'imageUrl': 'https://sh-s7-live-s.legocdn.com/is/image//LEGO/42083_alt1?$main$',
                'quantity': 1,
                'vatRate': '21.00',
                'unitPrice': {
                    'currency': 'EUR',
                    'value': '399.00'
                },
                'totalAmount': {
                    'currency': 'EUR',
                    'value': '698.00'
                },
                'discountAmount': {
                    'currency': 'EUR',
                    'value': '100.00'
                },
                'vatAmount': {
                    'currency': 'EUR',
                    'value': '121.14'
                }
            },

        ]
    }
    order = client.orders.create(data)
    assert isinstance(order, Order)
    assert order.id == ORDER_ID


def test_update_order(client, response):
    """Update an existing order."""
    response.patch('https://api.mollie.com/v2/orders/{order_id}'.format(order_id=ORDER_ID), 'order_updated')

    data = {
        'billingAddress': {
            'streetAndNumber': 'Keizersgracht 313',
            'city': 'Amsterdam',
            'region': 'Noord-Holland',
            'postalCode': '1234AB',
            'country': 'NL',
            'title': 'Dhr',
            'givenName': 'Piet',
            'familyName': 'Mondriaan',
            'email': 'piet@mondriaan.com',
            'phone': '+31208202070'
        }
    }
    updated_order = client.orders.update(ORDER_ID, data)
    assert isinstance(updated_order, Order)
    assert updated_order.billing_address['givenName'] == 'Piet'


def test_cancel_order(client, response):
    """Cancel an existing order."""
    response.delete('https://api.mollie.com/v2/orders/{order_id}'.format(order_id=ORDER_ID), 'order_canceled', 200)

    canceled_order = client.orders.delete(ORDER_ID)
    assert isinstance(canceled_order, Order)
    assert canceled_order.is_canceled() is True
    assert canceled_order.is_cancelable is False


def test_cancel_order_lines(client, response):
    """Cancel a line of an order."""
    response.get('https://api.mollie.com/v2/orders/{order_id}'.format(order_id=ORDER_ID), 'order_single')
    response.delete('https://api.mollie.com/v2/orders/{order_id}/lines'.format(order_id=ORDER_ID), 'empty', 204)

    order = client.orders.get(ORDER_ID)
    line = next(order.lines)
    data = {
        'lines': [
            {
                'id': line.id,
                'quantity': line.quantity
            }
        ]
    }
    canceled = order.cancel_lines(data)
    assert canceled == {}
