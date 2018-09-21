from mollie.api.objects.refund import Refund

from .utils import assert_list_object


def test_list_refunds(client, response):
    """Retrieve a list of refunds."""
    response.get('https://api.mollie.com/v2/refunds', 'refunds_list')

    refunds = client.refunds.list()
    assert_list_object(refunds, Refund)
