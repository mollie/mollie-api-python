from mollie.api.objects.organisation import Organisation

ORGANISATION_ID = 'org_12345678'


def test_get_organisation(client, response):
    """Retrieve a single organisation."""
    response.get('https://api.mollie.com/v2/organisations/%s' % ORGANISATION_ID, 'organisation_single')

    organisation = client.organisations.get(ORGANISATION_ID)
    assert isinstance(organisation, Organisation)
    assert organisation.id == ORGANISATION_ID
    assert organisation.name == 'Mollie B.V.'
    assert organisation.email == 'info@mollie.com'
    assert organisation.vat_number == 'NL815839091B01'
    assert organisation.registration_number == '30204462'
    assert organisation.address == {
        'city': 'Amsterdam',
        'country': 'NL',
        'postalCode': '1016 EE',
        'streetAndNumber': 'Keizersgracht 313'
    }


def test_get_current_organisation(client, response):
    """Retrieve a current organisation."""
    response.get('https://api.mollie.com/v2/organisations/me', 'organisation_current')

    organisation = client.organisations.get('me')
    assert isinstance(organisation, Organisation)
    assert organisation.id == ORGANISATION_ID
    assert organisation.name == 'Mollie B.V.'
    assert organisation.email == 'info@mollie.com'
    assert organisation.vat_number == 'NL815839091B01'
    assert organisation.registration_number == '30204462'
    assert organisation.address == {
        'city': 'Amsterdam',
        'country': 'NL',
        'postalCode': '1016 EE',
        'streetAndNumber': 'Keizersgracht 313'
    }
