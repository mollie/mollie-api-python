from mollie.api.objects.chargeback import Chargeback

from .utils import assert_list_object


def test_list_chargebacks(client, response):
    """Get a list of chargebacks."""
    response.get("https://api.mollie.com/v2/chargebacks", "chargebacks_list")
    response.get("https://api.mollie.com/v2/chargebacks?limit=1&from=chb_n9z0tq", "chargebacks_list_more")

    chargebacks = client.chargebacks.list()
    assert_list_object(chargebacks, Chargeback)

    assert chargebacks.has_next()
    more_chargebacks = chargebacks.get_next()
    assert_list_object(more_chargebacks, Chargeback)
