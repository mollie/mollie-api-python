from mollie.api.objects.capture import Capture

from .utils import assert_list_object


def test_list_chargebacks(client, response):
    """Get a list of chargebacks."""
    response.get('https://api.mollie.com/v2/payments/tr_WDqYK6vllg/captures', 'captures_list')
    captures = client.captures.with_parent_id('tr_WDqYK6vllg').list()
    assert_list_object(captures, Capture)
