# coding=utf-8

from __future__ import print_function

import json
import os

from flask import Flask
from flask import request

from mollie.api.client import Client

app = Flask(__name__)
client = Client()


def get_token():
    with open('token.json', 'r') as file:
        return json.loads(file.read())


def set_token(token):
    with open('token.json', 'w') as file:
        file.write(json.dumps(token))


Client.get_token = get_token
Client.set_token = set_token


@app.route('/')
def index():
    """
    FLASK_APP=examples/oauth/app.py CLIENT_ID=app_TuUwqdU76H8kFaB5hsrVGdMp CLIENT_SECRET=BrQfR325hwGg84jfNSBBM66BF9jg7hatC8EWrKDg REDIRECT_URI=https://9a334898.ngrok.io/callback flask run
    """

    help_text = "FLASK_APP=examples/oauth/app.py " \
                "CLIENT_ID=[your mollie client id] " \
                "CLIENT_SECRET=[your mollie client secret] " \
                "REDIRECT_URI=[your redirect uri] " \
                "flask run"

    client_id = os.environ.get('CLIENT_ID')
    assert bool(client_id), 'You have to set MOLLIE_CLIENT_ID. ' + help_text
    client_secret = os.environ.get('CLIENT_SECRET')
    assert bool(client_secret), 'You have to set CLIENT_SECRET. ' + help_text
    redirect_uri = os.environ.get('REDIRECT_URI')
    assert bool(redirect_uri), 'You have to set REDIRECT_URI. ' + help_text

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

    global client
    authorization_url = client.setup_oauth(
        client_id,
        client_secret,
        redirect_uri,
        scope,
        get_token,
        set_token,
    )
    body = '<h1>Your applications config panel</h1>'
    body += '<a href="{authorization_url}">{authorization_url}</a>'.format(authorization_url=authorization_url)
    return body


@app.route('/callback')
def callback(*args, **kwargs):
    global client

    url = request.url.replace('http', 'https')  # This fakes httpS. DONT DO THIS!
    client.setup_oauth_authorization_response(url)

    print(client.profiles.list())
    print(client.invoices.list())

    return '200 OK'  # 200 OK
