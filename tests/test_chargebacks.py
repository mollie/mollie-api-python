from responses import matchers

from mollie.api.objects.chargeback import Chargeback

from .utils import assert_list_object


def test_list_chargebacks(client, response):
    """Get a list of chargebacks."""
    response.get("https://api.mollie.com/v2/chargebacks", "chargebacks_list")

    chargebacks = client.chargebacks.list()
    assert_list_object(chargebacks, Chargeback)


def test_list_chargeback_pagination(client, response):
    """Retrieve a list of paginated chargebacks."""
    response.get(
        "https://api.mollie.com/v2/chargebacks", "chargebacks_list", match=[matchers.query_string_matcher("")]
    )
    response.get(
        "https://api.mollie.com/v2/chargebacks",
        "chargebacks_list_more",
        match=[matchers.query_string_matcher("from=chb_n9z0tq")],
    )

    first_chargebacks_page = client.chargebacks.list()
    assert first_chargebacks_page.has_previous() is False
    assert first_chargebacks_page.has_next() is True

    second_chargebacks_page = first_chargebacks_page.get_next()
    assert_list_object(second_chargebacks_page, Chargeback)

    subscription = next(second_chargebacks_page)
    assert subscription.id == "chb_n9z0tq"
