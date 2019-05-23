from mollie.api.objects.chargeback import Chargeback

from .utils import assert_list_object

PAYMENT_ID = 'tr_7UhSN1zuXS'
SETTLEMENT_ID = 'stl_jDk30akdN'
CHARGEBACK_ID = 'chb_n9z0tp'


def test_get_settlement_chargebacks_by_chargeback_id(client, response):
    """Get chargebacks relevant to settlement by settlement id."""
    response.get('https://api.mollie.com/v2/settlements/%s/chargebacks' % CHARGEBACK_ID, 'chargebacks_list')

    chargebacks = client.settlement_chargebacks.with_parent_id(CHARGEBACK_ID).list()
    assert_list_object(chargebacks, Chargeback)


def test_list_payment_settlement_by_payment_object(client, response):
    """Get a list of chargebacks relevant to settlement object."""
                  https://api.mollie.com/v2/settlements/stl_jDk30akdN
    response.get('https://api.mollie.com/v2/settlements/%s/chargebacks' % CHARGEBACK_ID, 'chargebacks_list')
    response.get('https://api.mollie.com/v2/settlements/%s' % SETTLEMENT_ID, 'settlement_single')


    settlement = client.settlements.get(SETTLEMENT_ID)
    chargebacks = client.settlement_chargebacks.on(settlement).list()
    assert_list_object(chargebacks, Chargeback)
