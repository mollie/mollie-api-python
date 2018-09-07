from mollie.api.objects.chargeback import Chargeback

from .utils import assert_list_object


def test_list_chargebacks(client, response):
    """Get a list of chargebacks."""
    response.get('https://api.mollie.com/v2/chargebacks', 'chargebacks_list')

    chargebacks = client.chargebacks.list()
    assert_list_object(chargebacks, Chargeback)
