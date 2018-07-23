def test_create_customers(client, response):
    response.post('https://api.mollie.com/v2/customers', 'customer_new')
    customer = client.customers.create({
        'name': 'Customer A',
        'email': 'customer@example.org',
        'locale': 'nl_NL',
    })
    assert customer.name == 'Customer A'
    assert customer.email == 'customer@example.org'
    assert customer.id is not None
    assert customer.resource == 'customer'
    assert customer.created_at is not None
    assert customer.metadata is None
    assert customer.locale == 'nl_NL'
    assert customer.mode == 'test'


def test_update_customers(client, response):
    response.post('https://api.mollie.com/v2/customers/cst_8wmqcHMN4U', 'customer_updated')
    updated_customer = client.customers.update('cst_8wmqcHMN4U', {
        'name': 'Updated Customer A',
        'email': 'updated-customer@example.org',
    })
    assert updated_customer.name == 'Updated Customer A'
    assert updated_customer.email == 'updated-customer@example.org'


def test_delete_customers(client, response):
    response.delete('https://api.mollie.com/v2/customers/cst_8wmqcHMN4U', 'empty')
    deleted_customer = client.customers.delete('cst_8wmqcHMN4U')
    assert deleted_customer == {}


def test_customers_all(client, response):
    response.get('https://api.mollie.com/v2/customers', 'customer_multiple')
    customers = client.customers.all()
    assert customers.count == 3
    iterated = 0
    for customer in customers:
        iterated += 1
        assert customer.id is not None
        assert customer.mode is not None
        assert customer.resource is not None
        assert customer.name is not None
        assert customer.email is not None
        assert customer.locale is not None
        assert customer.created_at is not None
    assert iterated == 3
