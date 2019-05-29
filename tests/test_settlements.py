import json

from mollie.api.objects.settlement import Settlement
from tests.utils import assert_list_object

SETTLEMENT_ID = 'stl_jDk30akdN'


def test_list_settlements(client, response):
    """Get a list of chargebacks."""
    response.get('https://api.mollie.com/v2/settlements', 'settlements_list')

    settlements = client.settlements.list()
    assert_list_object(settlements, Settlement)


def test_settlement_get(client, response):
    """Retrieve a single payment method by ID."""
    response.get('https://api.mollie.com/v2/settlements/%s' % SETTLEMENT_ID, 'settlement_single')

    settlement = client.settlements.get(SETTLEMENT_ID)

    assert isinstance(settlement, Settlement)
    assert settlement.reference == '1234567.1804.03'
    assert settlement.created_at == '2018-04-06T06:00:01.0Z'
    assert settlement.settled_at == '2018-04-06T09:41:44.0Z'
    assert settlement.amount == {'currency': 'EUR', 'value': '39.75'}
    assert settlement.invoice_id == 'inv_FrvewDA3Pr'
    assert settlement.is_open() is True
    assert settlement.is_pending() is False
    assert settlement.is_canceled() is False
    assert settlement.is_failed() is False
    assert settlement.periods == json.loads("""{
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
            ]
        }
    }
    }"""
                                            )

    def test_settlement_get_next(client, response):
        """Retrieve the details of the current settlement that has not yet been paid out."""
        response.get('https://api.mollie.com/v2/settlements/next', 'settlement_next')

        settlement = client.settlements.get('next')

        assert isinstance(settlement, Settlement)
        assert settlement.created_at == '2018-04-06T06:00:01.0Z'
        assert settlement.settled_at is None
        assert settlement.amount == {'currency': 'EUR', 'value': '39.75'}

    def test_settlement_get_open(client, response):
        """Retrieve the details of the open balance of the organization. """
        response.get('https://api.mollie.com/v2/settlements/open', 'settlement_open')

        settlement = client.settlements.get('open')

        assert isinstance(settlement, Settlement)
        assert settlement.reference is None
        assert settlement.created_at == '2018-04-06T06:00:01.0Z'
        assert settlement.settled_at is None
        assert settlement.amount == {'currency': 'EUR', 'value': '39.75'}
