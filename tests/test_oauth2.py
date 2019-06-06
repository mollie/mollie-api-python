import logging

import requests
import responses

logging.basicConfig(level=logging.DEBUG)

token = None


# try:
#     import urlparse
# except ImportError:
#     import urllib.parse as urlparse


def get_token():
    return token


def set_token(tkn):
    global token
    token = tkn


@responses.activate
def test_oauth2(client):
    client_id = "app_TuUwqdU76H8kFaB5hsrVGdMp"
    client_secret = "BrQfR325hwGg84jfNSBBM66BF9jg7hatC8EWrKDg"
    redirect_uri = "https://9a334898.ngrok.io/callback"
    scope = [
        'payments.read',
        'payments.write',
        'refunds.read',
        'refunds.write',
        'customers.read',
        'customers.write',
        'mandates.read',
        'mandates.write',
        'subscriptions.read',
        'subscriptions.write',
        'profiles.read',
        'profiles.write',
        'invoices.read',
        'settlements.read',
        'orders.read',
        'orders.write',
        'shipments.read',
        'shipments.write',
        'organizations.read',
        'organizations.write',
        'onboarding.read',
        'onboarding.write',
    ]

    authorized, authorization_url = client.setup_oauth(
        client_id,
        client_secret,
        redirect_uri,
        scope,
        get_token(),
        set_token,
    )

    assert authorized is False

    responses.add(responses.GET,
                  authorization_url,
                  status=302,
                  body='https://9a334898.ngrok.io/callback?code=auth_9ErGAqmhP8BQfE7wegt4hzCgGSJde3&'
                       'state=7FH48tEqWxjftE1WukJ6nDop8TSV56'
                  )
    auth = requests.get(authorization_url)

    assert auth.status_code == 302

    return_url = "https://9a334898.ngrok.io/callback?code=auth_9ErGAqmhP8BQfE7wegt4hzCgGSJde3&state={}".format(
        client.oauth._state)

    responses.add(responses.POST,
                  "https://api.mollie.com/oauth2/tokens",
                  json={'access_token': 'access_TAMuTC9pzCgcFK3QhT4SsTbDDMAxmR',
                        'expires_in': 3600,
                        'token_type': 'bearer',
                        'scope': ['customers.read',
                                  'customers.write',
                                  'invoices.read',
                                  'mandates.read',
                                  'mandates.write',
                                  'onboarding.read', 'onboarding.write', 'orders.read',
                                  'orders.write', 'organizations.read', 'organizations.write',
                                  'payments.read', 'payments.write', 'profiles.read',
                                  'profiles.write', 'refunds.read', 'refunds.write',
                                  'settlements.read', 'shipments.read', 'shipments.write',
                                  'subscriptions.read', 'subscriptions.write'],
                        'refresh_token': 'refresh_dRxySys7864P8stakHe2GC9cxH2Knb',
                        'expires_at': 1559737808.54537})

    access_token = client.setup_oauth_authorization_response(return_url)

    assert get_token() == access_token

    client.oauth_refresh_token(client_id, get_token(), set_token)
