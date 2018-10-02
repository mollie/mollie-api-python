from mollie.api.objects.order_line import OrderLine

from .utils import assert_list_object

ORDER_ID = 'ord_pbjz8x'
LINE_ID = 'odl_dgtxyl'


def test_get_order_lines(client, response):
    """Retrieve lines of a single order by order ID."""
    response.get('https://api.mollie.com/v2/orders/{order_id}'.format(order_id=ORDER_ID), 'order_single')

    order = client.orders.get(ORDER_ID)
    lines = order.lines
    assert_list_object(lines, OrderLine)

    # Test properties of the first line
    line = next(lines)
    assert isinstance(line, OrderLine)
    assert line.id == LINE_ID
    assert line.resource == 'orderline'
    assert line.order_id == ORDER_ID
    assert line.type == 'physical'
    assert line.name == 'LEGO 42083 Bugatti Chiron'
    assert line.status == 'created'
    assert line.is_cancelable is True
    assert line.quantity == 2
    assert line.shippable_quantity == 0
    assert line.quantity_shipped == 0
    assert line.amount_shipped == {'value': '0.00', 'currency': 'EUR'}
    assert line.refundable_quantity == 0
    assert line.quantity_refunded == 0
    assert line.amount_refunded == {'value': '0.00', 'currency': 'EUR'}
    assert line.cancelable_quantity == 0
    assert line.quantity_canceled == 0
    assert line.amount_canceled == {'value': '0.00', 'currency': 'EUR'}
    assert line.unit_price == {'value': '399.00', 'currency': 'EUR'}
    assert line.discount_amount == {'value': '100.00', 'currency': 'EUR'}
    assert line.total_amount == {'value': '698.00', 'currency': 'EUR'}
    assert line.vat_rate == '21.00'
    assert line.vat_amount == {'value': '121.14', 'currency': 'EUR'}
    assert line.sku == '5702016116977'
    assert line.image_url == 'https://sh-s7-live-s.legocdn.com/is/image//LEGO/42083_alt1?$main$'
    assert line.product_url == 'https://shop.lego.com/nl-NL/Bugatti-Chiron-42083'
    assert line.created_at == '2018-08-02T09:29:56+00:00'
    assert line.is_created() is True
    assert line.is_authorized() is False
    assert line.is_paid() is False
    assert line.is_shipping() is False
    assert line.is_canceled() is False
    assert line.is_completed() is False
