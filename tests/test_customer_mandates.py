CUSTOMER_ID = 'cst_8wmqcHMN4U'
MANDATE_ID = 'mdt_h3gAaD5zP'


def test_customer_mandates_all(client, response):
    """Retreive a list of mandates."""
    response.get('https://api.mollie.com/v2/customers/%s/mandates' % CUSTOMER_ID, 'customer_mandates_multiple')
    mandates = client.customer_mandates.with_parent_id(CUSTOMER_ID).all()
    assert mandates.__class__.__name__ == 'List'
    assert mandates.count == 1

    iterated = 0
    iterated_mandate_ids = []
    for mandate in mandates:
        assert mandate.__class__.__name__ == 'Mandate'
        iterated += 1
        assert mandate.id is not None
        iterated_mandate_ids.append(mandate.id)
    assert iterated == mandates.count, 'Unexpected amount of mandates retrieved'
    assert len(set(iterated_mandate_ids)) == mandates.count, 'Expected unique mandate ids retrieved'


def test_get_customer_mandate_by_id(client, response):
    """Retrieve a single mandate by ID."""
    response.get(
        'https://api.mollie.com/v2/customers/%s/mandates/%s' % (CUSTOMER_ID, MANDATE_ID),
        'customer_mandates_get',
    )

    mandate = client.customer_mandates.with_parent_id(CUSTOMER_ID).get(MANDATE_ID)
    assert mandate.id == MANDATE_ID
    assert mandate.resource == 'mandate'
    assert mandate.status == 'valid'
    assert mandate.method == 'directdebit'
    assert mandate.details == {
        'consumerName': 'John Doe',
        'consumerAccount': 'NL55INGB0000000000',
        'consumerBic': 'INGBNL2A',
    }
    assert mandate.mandate_reference == 'YOUR-COMPANY-MD1380'
    assert mandate.signature_date == '2018-05-07'
    assert mandate.created_at == '2018-05-07T10:49:08+00:00'
    assert mandate.is_pending() is False
    assert mandate.is_valid() is True
    assert mandate.is_invalid() is False


def test_get_customer_mandate_by_customer(client, response):
    """Retrieve a customer by customer object, ensure request is correct."""
    response.get('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_new')
    response.get('https://api.mollie.com/v2/customers/%s/mandates' % CUSTOMER_ID, 'customer_mandates_multiple')
    response.get(
        'https://api.mollie.com/v2/customers/%s/mandates/%s' % (CUSTOMER_ID, MANDATE_ID),
        'customer_mandates_get',
    )
    customer = client.customers.get(CUSTOMER_ID)

    mandates = client.customer_mandates.on(customer).all()
    assert MANDATE_ID in [x.id for x in mandates]

    mandate = client.customer_mandates.on(customer).get(MANDATE_ID)
    assert mandate.id == MANDATE_ID
