# import requests
import responses
import requests

token = None

import logging

logging.basicConfig(level=logging.DEBUG)

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


def get_token():
    return token


def set_token(tkn):
    global token
    token = tkn
    print(token)


@responses.activate
def test_oauth2(client): #, response):
    # responses.add()


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



    authorization_url = client.setup_oauth(
        client_id,
        client_secret,
        redirect_uri,
        scope,
        set_token,
    )

    # responses.add(responses.GET, authorization_url, body="https://9a334898.ngrok.io/callback?code=auth_9ErGAqmhP8BQfE7wegt4hzCgGSJde3&state=7FH48tEqWxjftE1WukJ6nDop8TSV56")
    # snarf = requests.get(authorization_url)

    # state = client.oauth._state

    return_url = "https://9a334898.ngrok.io/callback?code=auth_9ErGAqmhP8BQfE7wegt4hzCgGSJde3&state={}".format(client.oauth._state)
    # query = urlparse.urlparse(return_url).query
    # params = dict(urlparse.parse_qsl(query))
    #
    # client.oauth._state = params.get('state')




    # https://www.mollie.com/oauth2/authorize?response_type=code&client_id=app_TuUwqdU76H8kFaB5hsrVGdMp&redirect_uri=https%3A%2F%2F9a334898.ngrok.io%2Fcallback&scope=payments.read+payments.write+refunds.read+refunds.write+customers.read+customers.write+mandates.read+mandates.write+subscriptions.read+subscriptions.write+profiles.read+profiles.write+invoices.read+settlements.read+orders.read+orders.write+shipments.read+shipments.write+organizations.read+organizations.write+onboarding.read+onboarding.write&state=BAYdMSEw3NpeBmHxj0imUT4tDLUKl8

    # {"access_token":"access_TAMuTC9pzCgcFK3QhT4SsTbDDMAxmR","expires_in":3600,"token_type":"bearer","scope":"customers.read customers.write invoices.read mandates.read mandates.write onboarding.read onboarding.write orders.read orders.write organizations.read organizations.write payments.read payments.write profiles.read profiles.write refunds.read refunds.write settlements.read shipments.read shipments.write subscriptions.read subscriptions.write","refresh_token":"refresh_dRxySys7864P8stakHe2GC9cxH2Knb"}
    responses.add(responses.POST, "https://api.mollie.com/oauth2/tokens",  json={'access_token': 'access_TAMuTC9pzCgcFK3QhT4SsTbDDMAxmR', 'expires_in': 3600, 'token_type': 'bearer', 'scope': ['customers.read', 'customers.write', 'invoices.read', 'mandates.read', 'mandates.write', 'onboarding.read', 'onboarding.write', 'orders.read', 'orders.write', 'organizations.read', 'organizations.write', 'payments.read', 'payments.write', 'profiles.read', 'profiles.write', 'refunds.read', 'refunds.write', 'settlements.read', 'shipments.read', 'shipments.write', 'subscriptions.read', 'subscriptions.write'], 'refresh_token': 'refresh_dRxySys7864P8stakHe2GC9cxH2Knb', 'expires_at': 1559737808.54537})



    access_token = client.setup_oauth_authorization_response(return_url)
    set_token(access_token)

    assert get_token() == access_token

# (Pdb) get_token()
# {'access_token': 'access_TAMuTC9pzCgcFK3QhT4SsTbDDMAxmR', 'expires_in': 3600, 'token_type': 'bearer', 'scope': ['customers.read', 'customers.write', 'invoices.read', 'mandates.read', 'mandates.write', 'onboarding.read', 'onboarding.write', 'orders.read', 'orders.write', 'organizations.read', 'organizations.write', 'payments.read', 'payments.write', 'profiles.read', 'profiles.write', 'refunds.read', 'refunds.write', 'settlements.read', 'shipments.read', 'shipments.write', 'subscriptions.read', 'subscriptions.write'], 'refresh_token': 'refresh_dRxySys7864P8stakHe2GC9cxH2Knb', 'expires_at': 1559744453.144381}

    client.oauth_refresh_token( client_id, get_token(), set_token)

