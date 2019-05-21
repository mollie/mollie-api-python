from mollie.api.objects.onboarding import Onboarding


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
