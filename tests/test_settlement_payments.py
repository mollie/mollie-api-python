from mollie.api.objects.payment import Payment

from .utils import assert_list_object

SETTLEMENT_ID = 'stl_jDk30akdN'


def test_list_customer_payments(oauth_client, response):
    """Retrieve a list of payments related to a settlement id."""
    response.get('https://api.mollie.com/v2/settlements/%s/payments' % SETTLEMENT_ID, 'settlement_payments_multiple')

    payments = oauth_client.settlement_payments.with_parent_id(SETTLEMENT_ID).list()
    assert_list_object(payments, Payment)
