from mollie.api.objects.capture import Capture

from .utils import assert_list_object

PAYMENT_ID = 'tr_7UhSN1zuXS'


def test_list_chargebacks(client, response):
    """Get a list of chargebacks."""
    response.get('https://api.mollie.com/v2/payments/{}/captures'.format(PAYMENT_ID), 'captures_list')
    captures = client.captures.with_parent_id(PAYMENT_ID).list()
    assert_list_object(captures, Capture)
