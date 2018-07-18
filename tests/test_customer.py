import Mollie
import re


def test_create_customers(client, response):
    response.post('https://api.mollie.com/v2/customers', 'create_customer')
    customer = client.customers.create({
        'name': 'Customer A',
        'email': 'customer@example.org',
        'locale': 'nl_NL'
    })
    assert customer.name == 'Customer A'
    assert customer.email == 'customer@example.org'
    assert customer.id is not None
    assert customer.resource == 'customer'
    assert customer.createdAt is not None
    assert customer.metadata is None
    assert customer.locale == 'nl_NL'
    assert customer.mode is None
