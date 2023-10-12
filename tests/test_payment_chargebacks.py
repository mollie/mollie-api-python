import pytest
from responses import matchers

from mollie.api.error import IdentifierError
from mollie.api.objects.chargeback import Chargeback
from mollie.api.objects.payment import Payment
from mollie.api.objects.settlement import Settlement

from .utils import assert_list_object

PAYMENT_ID = "tr_7UhSN1zuXS"
CHARGEBACK_ID = "chb_n9z0tp"
SETTLEMENT_ID = "stl_jDk30akdN"


def test_list_payment_chargebacks(client, response):
    """Get chargebacks relevant to a payment."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/chargebacks", "payment_chargebacks_list")

    payment = client.payments.get(PAYMENT_ID)
    chargebacks = payment.chargebacks.list()
    assert_list_object(chargebacks, Chargeback)


def test_list_payment_chargebacks_pagination(client, response):
    """Retrieve a list of paginated payment chargebacks."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.get(
        f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/chargebacks",
        "payment_chargebacks_list",
        match=[matchers.query_string_matcher("")],
    )
    response.get(
        f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/chargebacks",
        "payment_chargebacks_list_more",
        match=[matchers.query_string_matcher("from=chb_n9z0tq")],
    )

    payment = client.payments.get(PAYMENT_ID)
    first_chargebacks_page = payment.chargebacks.list()
    assert first_chargebacks_page.has_previous() is False
    assert first_chargebacks_page.has_next() is True

    second_chargebacks_page = first_chargebacks_page.get_next()
    assert_list_object(second_chargebacks_page, Chargeback)

    subscription = next(second_chargebacks_page)
    assert subscription.id == "chb_n9z0tq"


def test_get_payment_chargeback(client, response):
    """Get a single chargeback relevant to a payment."""
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.get(
        f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/chargebacks/{CHARGEBACK_ID}", "payment_chargeback_single"
    )

    payment = client.payments.get(PAYMENT_ID)
    chargeback = payment.chargebacks.get(CHARGEBACK_ID)
    assert isinstance(chargeback, Chargeback)
    assert chargeback.id == CHARGEBACK_ID
    assert chargeback.amount == {"currency": "USD", "value": "43.38"}
    assert chargeback.settlement_amount == {"currency": "EUR", "value": "-35.07"}
    assert chargeback.created_at == "2018-03-14T17:00:52.0Z"
    assert chargeback.reason is None
    assert chargeback.reversed_at == "2018-03-14T17:00:55.0Z"
    assert chargeback.payment_id == PAYMENT_ID
    assert chargeback.settlement_id == SETTLEMENT_ID


def test_get_payment_chargeback_invalid_id(client, response):
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")

    payment = client.payments.get(PAYMENT_ID)
    with pytest.raises(IdentifierError) as excinfo:
        payment.chargebacks.get("invalid")
    assert str(excinfo.value) == "Invalid chargeback ID 'invalid', it should start with 'chb_'."


def test_payment_chargeback_get_related_payment(client, response):
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.get(
        f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/chargebacks/{CHARGEBACK_ID}", "payment_chargeback_single"
    )

    payment = client.payments.get(PAYMENT_ID)
    chargeback = payment.chargebacks.get(CHARGEBACK_ID)
    related_payment = chargeback.get_payment()
    assert isinstance(related_payment, Payment)
    assert related_payment.id == payment.id == PAYMENT_ID


def test_payment_chargeback_get_related_settlement(client, response):
    response.get(f"https://api.mollie.com/v2/payments/{PAYMENT_ID}", "payment_single")
    response.get(
        f"https://api.mollie.com/v2/payments/{PAYMENT_ID}/chargebacks/{CHARGEBACK_ID}", "payment_chargeback_single"
    )
    response.get(f"https://api.mollie.com/v2/settlements/{SETTLEMENT_ID}", "settlement_single")

    payment = client.payments.get(PAYMENT_ID)
    chargeback = payment.chargebacks.get(CHARGEBACK_ID)
    related_settlement = chargeback.get_settlement()
    assert isinstance(related_settlement, Settlement)
    assert related_settlement.id == SETTLEMENT_ID


@pytest.mark.parametrize(
    "url_settlement_id, actual_settlement_id",
    [
        (SETTLEMENT_ID, SETTLEMENT_ID),
        ("stl_j.k30akdN", "stl_j.k30akdN"),
        ("stl_j.k30akdN/", "stl_j.k30akdN"),  # trailing slash in URL
    ],
)
def test_payment_chargeback_get_related_settlement_id_syntax(url_settlement_id, actual_settlement_id, client):
    """Identifiers may have unexpected syntax."""
    data = {
        "resource": "chargeback",
        "id": "chb_n9z0tp",
        "_links": {
            "settlement": {
                "href": f"https://api.mollie.com/v2/settlements/{url_settlement_id}",
                "type": "application/hal+json",
            },
        },
    }
    chargeback = Chargeback(data, client)
    assert chargeback.settlement_id == actual_settlement_id
