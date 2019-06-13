from mollie.api.objects.onboarding import Onboarding
from mollie.api.objects.organization import Organization

ORGANIZATION_ID = 'org_12345678'


def test_get_onboarding(oauth_client, response):
    """Retrieve onboarding."""
    response.get('https://api.mollie.com/v2/onboarding/me', 'onboarding_me')

    onboarding = oauth_client.onboarding.get('me')
    assert isinstance(onboarding, Onboarding)

    assert onboarding.name == 'Mollie B.V.'
    assert onboarding.signed_up_at == '2018-12-20T10:49:08+00:00'
    assert onboarding.status == 'completed'
    assert onboarding.can_receive_payments is True
    assert onboarding.can_receive_settlements is True

    assert onboarding.is_needs_data() is False
    assert onboarding.is_in_review() is False
    assert onboarding.is_completed() is True


def test_create_onboarding(oauth_client, response):
    """Create onboarding."""
    response.post('https://api.mollie.com/v2/onboarding/me', 'empty', 204)

    data = {
        'profile': {
            'categoryCode': '6012'
        }
    }

    onboarding = oauth_client.onboarding.create(resource_id='me', data=data)
    assert isinstance(onboarding, Onboarding)


def test_onboarding_get_organization(oauth_client, response):
    """Retrieve organization related to onboarding."""
    response.get('https://api.mollie.com/v2/onboarding/me', 'onboarding_me')
    response.get('https://api.mollie.com/v2/organization/%s' % ORGANIZATION_ID, 'organization_single')

    onboarding = oauth_client.onboarding.get('me')
    organization = onboarding.organization
    assert isinstance(organization, Organization)
    assert organization.id == ORGANIZATION_ID
