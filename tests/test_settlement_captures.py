from mollie.api.objects.capture import Capture

from .utils import assert_list_object

PAYMENT_ID = 'tr_7UhSN1zuXS'
SETTLEMENT_ID = 'stl_jDk30akdN'
CHARGEBACK_ID = 'chb_n9z0tp'


def test_get_settlement_captures_by_capture_id(client, response):
    """Get chargebacks relevant to settlement by settlement id."""
    response.get('https://api.mollie.com/v2/settlements/%s/captures' % SETTLEMENT_ID, 'captures_list')

    captures = client.settlement_captures.with_parent_id(SETTLEMENT_ID).list()
    assert_list_object(captures, Capture)


def test_list_settlement_captures_by_capture_object(client, response):
    """Get a list of chargebacks relevant to settlement object."""
    response.get('https://api.mollie.com/v2/settlements/%s/captures' % SETTLEMENT_ID, 'captures_list')
    response.get('https://api.mollie.com/v2/settlements/%s' % SETTLEMENT_ID, 'settlement_single')

    settlement = client.settlements.get(SETTLEMENT_ID)
    captures = client.settlement_captures.on(settlement).list()
    assert_list_object(captures, Capture)
