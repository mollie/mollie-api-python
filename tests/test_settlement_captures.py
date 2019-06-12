from mollie.api.objects.capture import Capture

from .utils import assert_list_object

PAYMENT_ID = 'tr_7UhSN1zuXS'
SETTLEMENT_ID = 'stl_jDk30akdN'
CHARGEBACK_ID = 'chb_n9z0tp'


def test_get_settlement_captures_by_capture_id(oauth_client, response):
    """Get captures relevant to settlement by settlement id."""
    response.get('https://api.mollie.com/v2/settlements/%s/captures' % SETTLEMENT_ID, 'captures_list')

    captures = oauth_client.settlement_captures.with_parent_id(SETTLEMENT_ID).list()
    assert_list_object(captures, Capture)


def test_list_settlement_captures_by_capture_object(oauth_client, response):
    """Get a list of captures relevant to settlement object."""
    response.get('https://api.mollie.com/v2/settlements/%s/captures' % SETTLEMENT_ID, 'captures_list')
    response.get('https://api.mollie.com/v2/settlements/%s' % SETTLEMENT_ID, 'settlement_single')

    settlement = oauth_client.settlements.get(SETTLEMENT_ID)
    captures = oauth_client.settlement_captures.on(settlement).list()
    assert_list_object(captures, Capture)
