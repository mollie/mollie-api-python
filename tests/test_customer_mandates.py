from mollie.api.objects.customer import Customer
from mollie.api.objects.mandate import Mandate

from .utils import assert_list_object

CUSTOMER_ID = 'cst_8wmqcHMN4U'
MANDATE_ID = 'mdt_h3gAaD5zP'


def test_list_customer_mandates(client, response):
    """Retrieve a list of mandates."""
    response.get('https://api.mollie.com/v2/customers/%s/mandates' % CUSTOMER_ID, 'customer_mandates_list')
    mandates = client.customer_mandates.with_parent_id(CUSTOMER_ID).list()
    assert_list_object(mandates, Mandate)


def test_get_customer_mandate_by_id(client, response):
    """Retrieve a single mandate by ID."""
    response.get(
        'https://api.mollie.com/v2/customers/%s/mandates/%s' % (CUSTOMER_ID, MANDATE_ID),
        'customer_mandate_single',
    )
    response.get('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_new')

    mandate = client.customer_mandates.with_parent_id(CUSTOMER_ID).get(MANDATE_ID)
    assert isinstance(mandate, Mandate)
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
    assert mandate.customer is not None


def test_get_customer_mandate_by_customer(client, response):
    """Retrieve a customer by customer object."""
    response.get('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_new')
    response.get('https://api.mollie.com/v2/customers/%s/mandates' % CUSTOMER_ID, 'customer_mandates_list')
    response.get(
        'https://api.mollie.com/v2/customers/%s/mandates/%s' % (CUSTOMER_ID, MANDATE_ID),
        'customer_mandate_single',
    )
    customer = client.customers.get(CUSTOMER_ID)

    mandates = client.customer_mandates.on(customer).list()
    assert_list_object(mandates, Mandate)

    mandate = client.customer_mandates.on(customer).get(MANDATE_ID)
    assert isinstance(mandate, Mandate)
    assert mandate.id == MANDATE_ID


def test_customer_mandate_get_related_customer(client, response):
    """Retrieve a related customer object from a mandate."""
    response.get(
        'https://api.mollie.com/v2/customers/%s/mandates/%s' % (CUSTOMER_ID, MANDATE_ID),
        'customer_mandate_single',
    )
    response.get('https://api.mollie.com/v2/customers/%s' % CUSTOMER_ID, 'customer_new')

    mandate = client.customer_mandates.with_parent_id(CUSTOMER_ID).get(MANDATE_ID)
    assert isinstance(mandate.customer, Customer)
    assert mandate.customer.id == CUSTOMER_ID


def test_customer_mandates_create_mandate(client, response):
    """Create a new customer mandate."""
    response.post('https://api.mollie.com/v2/customers/%s/mandates' % CUSTOMER_ID, 'customer_mandate_single')

    data = {
        'method': 'directdebit',
        'consumerName': 'John Doe',
        'consumerAccount': 'NL55INGB0000000000',
        'consumerBic': 'INGBNL2A',
        'signatureDate': '2018-05-07',
        'mandateReference': 'YOUR-COMPANY-MD1380',
    }
    mandate = client.customer_mandates.with_parent_id(CUSTOMER_ID).create(data=data)
    assert isinstance(mandate, Mandate)
    assert mandate.id == MANDATE_ID


def test_update_customer_mandate(client, response):
    response.patch(
        'https://api.mollie.com/v2/customers/%s/mandates/%s' % (CUSTOMER_ID, MANDATE_ID),
        'customer_mandate_updated'
    )

    data = {
        'method': 'directdebit',
        'consumerName': 'John Doe',
        'consumerAccount': 'NL09ASNB0000000000',
        'consumerBic': 'ASNBNL21',
        'signatureDate': '2018-05-07',
        'mandateReference': 'OTHER-COMPANY-12345',
    }
    mandate = client.customer_mandates.with_parent_id(CUSTOMER_ID).update(MANDATE_ID, data=data)
    assert isinstance(mandate, Mandate)
    assert mandate.id == MANDATE_ID
