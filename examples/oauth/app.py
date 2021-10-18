import json
import os

import flask
from flask import Flask, redirect, request, url_for

from mollie.api.client import Client

app = Flask(__name__)
client = Client()


def get_token():
    """
    :return: token (dict) or None
    """
    if os.path.exists("token.json"):
        with open("token.json", "r") as file:
            return json.loads(file.read())


def set_token(token):
    """
    :param token: token (dict)
    :return: None
    """
    with open("token.json", "w") as file:
        file.write(json.dumps(token))


examples = [
    "01-invoices",
    "02-onboarding",
    "03-organizations",
    "04-permissions",
    "05-profiles",
    "06-settlements",
]


@app.route("/")
def index():
    """
    FLASK_APP=examples/oauth/app.py \
    MOLLIE_CLIENT_ID=your_client_id \
    MOLLIE_CLIENT_SECRET=your_client_secret \
    MOLLIE_PUBLIC_URL=https://your_domain.tld \
    flask run
    """

    client_id = os.environ.get("MOLLIE_CLIENT_ID")
    client_secret = os.environ.get("MOLLIE_CLIENT_SECRET")
    public_url = os.environ.get("MOLLIE_PUBLIC_URL")
    redirect_uri = f"{public_url}/callback"

    scope = [
        "payments.read",
        "payments.write",
        "refunds.read",
        "refunds.write",
        "customers.read",
        "customers.write",
        "mandates.read",
        "mandates.write",
        "subscriptions.read",
        "subscriptions.write",
        "profiles.read",
        "profiles.write",
        "invoices.read",
        "settlements.read",
        "orders.read",
        "orders.write",
        "shipments.read",
        "shipments.write",
        "organizations.read",
        "organizations.write",
        "onboarding.read",
        "onboarding.write",
    ]

    global client

    authorized, authorization_url = client.setup_oauth(
        client_id,
        client_secret,
        redirect_uri,
        scope,
        get_token(),
        set_token,
    )

    if not authorized:
        body = "<h1>Your applications config panel</h1>"
        body += f'<a href="{authorization_url}">{authorization_url}</a>'
        return body
    return redirect(url_for("examples_view"))


@app.route("/callback")
def callback(*args, **kwargs):
    global client

    url = request.url.replace("http", "https")  # This fakes httpS. DONT DO THIS!
    client.setup_oauth_authorization_response(url)
    body = "<h1>Oauth client is setup</h1>"
    body += '<a href="/examples">Examples</a></p>'
    return body


@app.route("/examples")
def examples_view():
    body = "<h1>Examples</h1><ul>"
    for example in examples:
        body += f'<li><a href="/{example}">{example}</a></li>'
    body += "</ul>"
    return body


@app.route("/<example>", methods=["GET", "POST"])
def run_example(example=None):
    if example not in examples:
        flask.abort(404, "Example does not exist")
    return __import__(example).main(client)


if __name__ == "__main__":
    app.debug = True
    app.run()
