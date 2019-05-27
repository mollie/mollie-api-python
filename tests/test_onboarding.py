from mollie.api.objects.onboarding import Onboarding
from mollie.api.objects.organisation import Organisation

ORGANISATION_ID = 'org_12345678'


def test_get_onboarding(client, response):
    """Retrieve onboarding."""
    response.get('https://api.mollie.com/v2/onboarding/me', 'onboarding_me')

    onboarding = client.onboarding.get('me')
    assert isinstance(onboarding, Onboarding)

    assert onboarding.name == 'Mollie B.V.'
    assert onboarding.signed_up_at == '2018-12-20T10:49:08+00:00'
    assert onboarding.status == 'completed'
    assert onboarding.can_receive_payments is True
    assert onboarding.can_receive_settlements is True


def test_create_onboarding(client, response):
    """Update onboarding.."""
    response.patch('https://api.mollie.com/v2/onboarding/me', 'empty', 204)

    data = {
        'profile': {
            'categoryCode': '6012'
        }
    }

    onboarding = client.onboarding.update(resource_id='me', data=data)
    assert isinstance(onboarding, Onboarding)


def test_onboarding_get_organisation(client, response):
    """Retrieve organisation related to onboarding."""
    response.get('https://api.mollie.com/v2/onboarding/me', 'onboarding_me')
    response.get('https://api.mollie.com/v2/organization/%s' % ORGANISATION_ID, 'organisation_single')

    onboarding = client.onboarding.get('me')
    organisation = onboarding.organisation
    assert isinstance(organisation, Organisation)
    assert organisation.id == ORGANISATION_ID
