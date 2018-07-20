BOOLEANS = [True, False]


def test_payments_all(client, response):
    response.get('https://api.mollie.com/v2/payments', 'payments_multiple')

    payments = client.payments.all()
    assert payments.count == 3
    iterated = 0
    for payment in payments:
        iterated += 1
        assert payment.isOpen in BOOLEANS
        assert payment.isPending in BOOLEANS
        assert payment.isCanceled in BOOLEANS
        assert payment.isExpired in BOOLEANS
        assert payment.isPaid in BOOLEANS
        assert payment.isFailed in BOOLEANS
        assert payment.resource == "payment"
        assert payment.id is not None
        assert payment.mode == "test"
        assert payment.createdAt is not None
        assert payment.amount['value'] is not None
        assert payment.amount['currency'] is not None
        assert payment.description is not None
        assert payment.method is not None
        assert payment.metadata['order_nr'] is not None
        assert payment.status is not None
        assert payment.isCancelable in BOOLEANS
        assert payment.expiresAt is not None
        assert payment.profileId is not None
        assert payment.sequenceType is not None
        assert payment.redirectUrl is not None
        assert payment.webhookUrl is not None
        assert payment.settlementAmount['value'] is not None
        assert payment.settlementAmount['currency'] is not None

    assert iterated == 3


def test_create_payment(client, response):
    response.post('https://api.mollie.com/v2/payments', 'payments_create')
    payment = client.payments.create(
        {
            'amount': {'currency': 'EUR', 'value': '10.00'},
            'description': 'Order #12345',
            'redirectUrl': 'https://webshop.example.org/order/12345/',
            'webhookUrl': 'https://webshop.example.org/payments/webhook/',
            'method': 'ideal',
        })
    assert payment.amount['value'] == '10.00'
    assert payment.amount['currency'] == 'EUR'
    assert payment.description == 'Order #12345'
    assert payment.redirectUrl == 'https://webshop.example.org/order/12345/'
    assert payment.webhookUrl == 'https://webshop.example.org/payments/webhook/'
    assert payment.isCancelable is False
    assert payment.createdAt is not None
    assert payment.expiresAt is not None
    assert payment.profileId is not None
    assert payment.method == 'ideal'
    assert payment.metadata['order_id'] == '12345'
    assert payment.sequenceType == 'oneoff'
    assert payment.profileId == 'pfl_QkEhN94Ba'
    assert payment.isOpen in BOOLEANS
    assert payment.isPending in BOOLEANS
    assert payment.isCanceled in BOOLEANS
    assert payment.isExpired in BOOLEANS
    assert payment.isPaid in BOOLEANS
    assert payment.isFailed in BOOLEANS
