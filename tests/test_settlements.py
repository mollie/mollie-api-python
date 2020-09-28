import json

import pytest

from mollie.api.error import APIDeprecationWarning, IdentifierError
from mollie.api.objects.settlement import Settlement
from mollie.api.resources.settlements import Settlements
from tests.utils import assert_list_object

SETTLEMENT_ID = 'stl_jDk30akdN'


def test_list_settlements(oauth_client, response):
    """Get a list of settlements."""
    response.get('https://api.mollie.com/v2/settlements', 'settlements_list')

    settlements = oauth_client.settlements.list()
    assert_list_object(settlements, Settlement)


def test_settlement_get(oauth_client, response):
    """Retrieve a single settlement method by ID."""
    response.get('https://api.mollie.com/v2/settlements/%s' % SETTLEMENT_ID, 'settlement_single')
    response.get('https://api.mollie.com/v2/settlements/%s/chargebacks' % SETTLEMENT_ID, 'chargebacks_list')
    response.get('https://api.mollie.com/v2/settlements/%s/payments' % SETTLEMENT_ID, 'settlement_payments_multiple')
    response.get('https://api.mollie.com/v2/settlements/%s/refunds' % SETTLEMENT_ID, 'refunds_list')

    settlement = oauth_client.settlements.get(SETTLEMENT_ID)
    chargebacks = oauth_client.settlement_chargebacks.with_parent_id(SETTLEMENT_ID).list()
    payments = oauth_client.settlement_payments.with_parent_id(SETTLEMENT_ID).list()
    refunds = oauth_client.settlement_refunds.with_parent_id(SETTLEMENT_ID).list()

    assert isinstance(settlement, Settlement)

    assert settlement.periods == json.loads(
        """{
            "2018": {
                "4": {
                    "revenue": [
                        {
                            "description": "iDEAL",
                            "method": "ideal",
                            "count": 6,
                            "amountNet": {
                                "currency": "EUR",
                                "value": "86.1000"
                            },
                            "amountVat": null,
                            "amountGross": {
                                "currency": "EUR",
                                "value": "86.1000"
                            }
                        },
                        {
                            "description": "Refunds iDEAL",
                            "method": "refund",
                            "count": 2,
                            "amountNet": {
                                "currency": "EUR",
                                "value": "-43.2000"
                            },
                            "amountVat": null,
                            "amountGross": {
                                "currency": "EUR",
                                "value": "43.2000"
                            }
                        }
                    ],
                    "costs": [
                        {
                            "description": "iDEAL",
                            "method": "ideal",
                            "count": 6,
                            "rate": {
                                "fixed": {
                                    "currency": "EUR",
                                    "value": "0.3500"
                                },
                                "percentage": null
                            },
                            "amountNet": {
                                "currency": "EUR",
                                "value": "2.1000"
                            },
                            "amountVat": {
                                "currency": "EUR",
                                "value": "0.4410"
                            },
                            "amountGross": {
                                "currency": "EUR",
                                "value": "2.5410"
                            }
                        },
                        {
                            "description": "Refunds iDEAL",
                            "method": "refund",
                            "count": 2,
                            "rate": {
                                "fixed": {
                                    "currency": "EUR",
                                    "value": "0.2500"
                                },
                                "percentage": null
                            },
                            "amountNet": {
                                "currency": "EUR",
                                "value": "0.5000"
                            },
                            "amountVat": {
                                "currency": "EUR",
                                "value": "0.1050"
                            },
                            "amountGross": {
                                "currency": "EUR",
                                "value": "0.6050"
                            }
                        }
                    ],
                    "invoiceId": "inv_FrvewDA3Pr"
                }
            }
        }"""
    )

    assert settlement.reference == '1234567.1804.03'
    assert settlement.created_at == '2018-04-06T06:00:01.0Z'
    assert settlement.settled_at == '2018-04-06T09:41:44.0Z'
    assert settlement.amount == {'currency': 'EUR', 'value': '39.75'}

    assert settlement.status == settlement.STATUS_OPEN
    assert settlement.is_open() is True
    assert settlement.is_canceled() is False
    assert settlement.is_failed() is False
    assert settlement.is_pending() is False

    assert settlement.chargebacks == chargebacks
    assert settlement.payments == payments
    assert settlement.refunds == refunds


def test_settlement_get_next(oauth_client, response):
    """Retrieve the details of the current settlement that has not yet been paid out."""
    response.get('https://api.mollie.com/v2/settlements/next', 'settlement_next')

    settlement = oauth_client.settlements.get('next')

    assert isinstance(settlement, Settlement)
    assert settlement.created_at == '2018-04-06T06:00:01.0Z'
    assert settlement.settled_at is None
    assert settlement.amount == {'currency': 'EUR', 'value': '39.75'}


def test_settlement_get_open(oauth_client, response):
    """Retrieve the details of the open balance of the organization."""
    response.get('https://api.mollie.com/v2/settlements/open', 'settlement_open')

    settlement = oauth_client.settlements.get('open')

    assert isinstance(settlement, Settlement)
    assert settlement.reference is None
    assert settlement.created_at == '2018-04-06T06:00:01.0Z'
    assert settlement.settled_at is None
    assert settlement.amount == {'currency': 'EUR', 'value': '39.75'}


@pytest.mark.parametrize(
    "input,expected",
    [
        (None, IdentifierError),
        ("foo", IdentifierError),
        ("next", None),  # Valid
        ("open", None),  # Valid
        (SETTLEMENT_ID, None),  # Valid
        ("1234567.1234.12", None)  # Valid
    ]
)
def test_validate_settlement_id(input, expected):
    """Ensure that we only accept correctly formatted settlement IDs."""
    if expected == IdentifierError:
        with pytest.raises(IdentifierError):
            Settlements.validate_settlement_id(input)
    else:
        assert Settlements.validate_settlement_id(input) is expected


def test_settlement_invoice_id_is_deprecated(oauth_client, response):
    response.get('https://api.mollie.com/v2/settlements/%s' % SETTLEMENT_ID, 'settlement_single')

    settlement = oauth_client.settlements.get(SETTLEMENT_ID)
    with pytest.warns(APIDeprecationWarning, match='Using Settlement Invoice ID is deprecated'):
        assert settlement.invoice_id == "inv_FrvewDA3Pr"
