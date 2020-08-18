from mollie.api.objects.refund import Refund
from mollie.api.objects.settlement import Settlement

from .utils import assert_list_object

SETTLEMENT_ID = 'stl_jDk30akdN'


def test_list_refunds_on_settlement_object(oauth_client, response):
    """Retrieve a list of payment refunds of a payment."""
    response.get('https://api.mollie.com/v2/settlements/%s' % SETTLEMENT_ID, 'settlement_single')
    response.get('https://api.mollie.com/v2/settlements/%s/refunds' % SETTLEMENT_ID, 'refunds_list')

    settlement = oauth_client.settlements.get(SETTLEMENT_ID)
    assert isinstance(settlement, Settlement)

    refunds = oauth_client.settlement_refunds.on(settlement).list()
    assert_list_object(refunds, Refund)
