from mollie.api.objects.chargeback import Chargeback
from mollie.api.objects.list import List


def test_get_all_chargebacks(client, response):
    """Get all chargebacks."""
    response.get('https://api.mollie.com/v2/chargebacks', 'chargebacks_list')

    chargebacks = client.chargebacks.all()
    assert chargebacks.count == 1
    assert isinstance(chargebacks, List)

    iterated = 0
    iterated_chargeback_ids = []
    for chargeback in chargebacks:
        assert isinstance(chargeback, Chargeback)
        assert chargeback.id is not None
        iterated += 1
        iterated_chargeback_ids.append(chargeback.id)
    assert iterated == chargebacks.count, 'Unexpected amount of chargebacks retrieved'
    assert len(
        set(iterated_chargeback_ids)) == chargebacks.count, 'Unexpected amount of unique chargeback ids retrieved'
