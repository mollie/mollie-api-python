from mollie.api.objects.settlement import Settlement
from tests.utils import assert_list_object

SETTLEMENT_ID = 'stl_jDk30akdN'


def test_list_settlements(client, response):
    """Get a list of chargebacks."""
    response.get('https://api.mollie.com/v2/settlements', 'settlements_list')

    settlements = client.settlements.list()
    assert_list_object(settlements, Settlement)


def test_settlement_get(client, response):
    """Retrieve a single payment method by ID."""
    response.get('https://api.mollie.com/v2/settlements/%s' % SETTLEMENT_ID, 'settlement_single')

    settlement = client.settlements.get(SETTLEMENT_ID)

    assert isinstance(settlement, Settlement)
    assert settlement.reference == '1234567.1804.03'
    assert settlement.created_at == '2018-04-06T06:00:01.0Z'
    assert settlement.settled_at == '2018-04-06T09:41:44.0Z'
    assert settlement.amount == {'currency': 'EUR', 'value': '39.75'}
    assert settlement.invoice_id == 'inv_FrvewDA3Pr'


def test_settlement_get_next(client, response):
    """Retrieve the details of the current settlement that has not yet been paid out."""
    response.get('https://api.mollie.com/v2/settlements/next', 'settlement_next')

    settlement = client.settlements.get('next')

    assert isinstance(settlement, Settlement)
    assert settlement.created_at == '2018-04-06T06:00:01.0Z'
    assert settlement.settled_at is None
    assert settlement.amount == {'currency': 'EUR', 'value': '39.75'}


def test_settlement_get_open(client, response):
    """Retrieve the details of the open balance of the organization. """
    response.get('https://api.mollie.com/v2/settlements/open', 'settlement_open')

    settlement = client.settlements.get('open')

    assert isinstance(settlement, Settlement)
    assert settlement.reference is None
    assert settlement.created_at == '2018-04-06T06:00:01.0Z'
    assert settlement.settled_at is None
    assert settlement.amount == {'currency': 'EUR', 'value': '39.75'}
