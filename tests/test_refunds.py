from mollie.api.objects.list import List
from mollie.api.objects.refund import Refund


def test_list_all_refunds(client, response):
    """Retrieve a list of all refunds"""
    response.get('https://api.mollie.com/v2/refunds', 'refunds_multiple')
    refunds = client.refunds.all()
    assert refunds.count == 1
    assert isinstance(refunds, List)

    iterated = 0
    iterated_refund_ids = []
    for refund in refunds:
        assert isinstance(refund, Refund)
        iterated += 1
        assert refund.id is not None
        iterated_refund_ids.append(refund.id)
    assert iterated == refunds.count, 'Unexpected amount of refunds retrieved'
    assert len(set(iterated_refund_ids)) == refunds.count, 'Unexpected unique refund ids retrieved'


