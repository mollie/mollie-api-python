<p align="center">
  <img src="https://info.mollie.com/hubfs/github/python/logo.png" width="128" height="128"/>
</p>
<h1 align="center">Mollie API client for Python</h1>

<img src="https://info.mollie.com/hubfs/github/python/editor-1.png" />

Accepting [iDEAL](https://www.mollie.com/en/payments/ideal/), [Bancontact/Mister Cash](https://www.mollie.com/en/payments/bancontact/), [SOFORT Banking](https://www.mollie.com/en/payments/sofort/), [Creditcard](https://www.mollie.com/en/payments/credit-card/), [SEPA Bank transfer](https://www.mollie.com/en/payments/bank-transfer/), [SEPA Direct debit](https://www.mollie.com/en/payments/direct-debit/), [PayPal](https://www.mollie.com/en/payments/paypal/), [Belfius Direct Net](https://www.mollie.com/en/payments/belfius/), [KBC/CBC](https://www.mollie.com/en/payments/kbc-cbc/), Klarna [Pay later](https://www.mollie.com/en/payments/klarna-pay-later/)/[Pay now](https://www.mollie.com/en/payments/klarna-pay-now/)/[Slice it](https://www.mollie.com/en/payments/klarna-slice-it/), [paysafecard](https://www.mollie.com/en/payments/paysafecard/), [Giftcards](https://www.mollie.com/en/payments/gift-cards/), [Giropay](https://www.mollie.com/en/payments/giropay/), [EPS](https://www.mollie.com/en/payments/eps/), [Przelewy24](https://www.mollie.com/en/payments/przelewy24) and [Billie](https://www.mollie.com/en/payments/billie) online payments without fixed monthly costs or any punishing registration procedures. Just use the Mollie API to receive payments directly on your website or easily refund transactions to your customers.

[![PyPI version](https://badge.fury.io/py/mollie-api-python.svg)](http://badge.fury.io/py/mollie-api-python)
![Tests](https://github.com/mollie/mollie-api-python/actions/workflows/tests.yaml/badge.svg)

## Requirements ##
To use the Mollie API client, the following things are required:

+ Get yourself a free [Mollie account](https://my.mollie.com/dashboard/signup). No sign up costs.
+ Create a new [Website profile](https://www.mollie.com/dashboard/settings/profiles) to generate API keys and setup your webhook.
+ Now you're ready to use the Mollie API client in test mode.
+ Follow [a few steps](https://www.mollie.com/dashboard/?modal=onboarding) to enable payment methods in live mode, and let us handle the rest.
+ Python >= 3.8
+ Up-to-date OpenSSL (or other SSL/TLS toolkit)
+ Mollie API client for Python has a dependency on [Requests](http://docs.python-requests.org/en/master/) and [Requests-OAuthlib](https://requests-oauthlib.readthedocs.io/en/latest/)

## Migration to v3 ##
If your application uses a recent v2 version of the Mollie API client and you're ready to migrate to v3, [read all about the API changes](https://github.com/mollie/mollie-api-python/blob/master/v3-api-changes.md) that we made. Use the docs to quickly find how to update your integration code and use the v3 client correctly.

## Installation ##
**Please note:** If you want to install an older version of the Mollie API client (current major version is `v3`), then please refer to their respective github branches for installation instructions:
- version 2.x.x is available from the [v2-develop branch](https://github.com/mollie/mollie-api-python/tree/v2-develop).
- version 1.x.x is available from the [v1-develop branch](https://github.com/mollie/mollie-api-python/tree/v1-develop).

By far the easiest way to install the Mollie API client is to install it with [pip](https://pip.pypa.io). The command below will install the latest released version of the client.
```shell
$ pip install mollie-api-python
```
You may also git checkout or [download all the files](https://github.com/mollie/mollie-api-python/archive/master.zip), and include the Mollie API client manually.

Create and activate a Python >= 3.8 virtual environment (inside a git checkout or downloaded archive).

```shell
$ cd mollie-api-python
$ python -m venv .venv
$ source .venv/bin/activate
```

Install the additional requirements for the examples, then install the Mollie API client itself.
```shell
$ pip install flask
$ pip install -e .
```

Run the examples.
```shell
export MOLLIE_API_KEY=test_YourApiKey
$ python examples/app.py
```

If you are working from a development machine, you should use a tool like [ngrok.com](https://ngrok.com/) to get a publicly available URL that can be used in callback and redirect URLs. Start the service and expose the forwarding URL (https) to the mollie example code:

```shell
export MOLLIE_API_KEY=test_YourApiKey
export MOLLIE_PUBLIC_URL=https://some.ngrok.url.io
$ python examples/app.py
```

## How to receive payments ##

To successfully receive a payment, these steps should be implemented:

1. Use the Mollie API client to create a payment with the requested amount, currency, description and optionally, a payment method. It is important to specify a unique redirect URL where the customer is supposed to return to after the payment is completed.

2. Immediately after the payment is completed, our platform will send an asynchronous request to the configured webhook to allow the payment details to be retrieved, so you know when exactly to start processing the customer's order.

3. The customer returns, and should be satisfied to see that the order was paid and is now being processed.

Find our full documentation online on [docs.mollie.com](https://docs.mollie.com).

## Getting started ##

Importing the Mollie API Client
```python
from mollie.api.client import Client
``` 
Initializing the Mollie API client, and setting your API key

```python
mollie_client = Client()
mollie_client.set_api_key('test_dHar4XY7LxsDOtmnkVtjNVWXLSlXsM')
``` 

Creating a new payment.

```python
payment = mollie_client.payments.create({
    'amount': {
        'currency': 'EUR',
        'value': '10.00' 
    },
    'description': 'My first API payment',
    'redirectUrl': 'https://webshop.example.org/order/12345/',
    'webhookUrl': 'https://webshop.example.org/mollie-webhook/',
})
```
_After creation, the payment id is available in the `payment.id` property. You should store this id with your order._

After storing the payment id you can send the customer to the checkout using the `payment.checkout_url`.  

For a payment create example, see [Example 1 - New Payment](https://github.com/mollie/mollie-api-python/blob/master/examples/01-new-payment.py).

In general, request body parameters for an API endpoint should be added to a dictionary and provided as the first argument (or `data` keyword argument). Query string parameters can be provided as keyword arguments.

## Retrieving payments ##
We can use the `payment.id` to retrieve a payment and check if the payment `isPaid`.

```python
payment = mollie_client.payments.get(payment.id)

if payment.is_paid():
    print('Payment received.')
```

Or retrieve a collection of payments.

```python
payments = mollie_client.payments.list()
```

For an extensive example of listing payments with the details and status, see [Example 5 - Payments History](https://github.com/mollie/mollie-api-python/blob/master/examples/05-payments-history.py).

## Payment webhook ##

When the status of a payment changes the `webhookUrl` we specified in the creation of the payment will be called.  
There we can use the `id` from our POST parameters to check te status and act upon that, see [Example 2 - Webhook verification](https://github.com/mollie/mollie-api-python/blob/master/examples/02-webhook-verification.py).


## Multicurrency ##
Since the 2.0 version of the API (supported by version 2.0.0 of the client) non-EUR payments for your customers is now supported.
A full list of available currencies can be found [in our documentation](https://docs.mollie.com/guides/multicurrency).

```python
payment = mollie_client.payments.create({
    'amount': {
        'currency': 'USD', 
        'value': '10.00'
    },
    'description': 'Order #12345',
    'redirectUrl': 'https://webshop.example.org/order/12345/',
    'webhookUrl': 'https://webshop.example.org/mollie-webhook/',
})
```
_After the customer completes the payment, the `payment.settlement_amount` will contain the amount + currency that will be settled on your account._

### Fully integrated iDEAL payments ###

If you want to fully integrate iDEAL payments in your web site, some additional steps are required. 
First, you need to retrieve the list of issuers (banks) that support iDEAL and have your customer pick the issuer 
he/she wants to use for the payment.

Retrieve the iDEAL method and include the issuers

```python
method = mollie_client.methods.get(mollie.api.objects.Method.IDEAL, include='issuers')
```

_`method.issuers` will be a list of Issuer objects. Use the property `id` of this object in the
 API call, and the property `name` for displaying the issuer to your customer. For a more in-depth example, see [Example 4 - iDEAL payment](https://github.com/mollie/mollie-api-python/blob/master/examples/04-ideal-payment.py)._

```python
payment = mollie_client.payments.create({
    'amount': {
        'currency': 'EUR', 
        'value': '10.00'
    },
    'description': 'My first API payment',
    'redirectUrl': 'https://webshop.example.org/order/12345/',
    'webhookUrl': 'https://webshop.example.org/mollie-webhook/',
    'method': mollie.api.objects.Method.IDEAL,
    'issuer': selectedIssuerId,  # e.g. "ideal_INGBNL2A"
})
```
The `payment.checkout_url` is a URL that points directly to the online banking environment of the selected issuer.

### Refunding payments ###

The API also supports refunding payments. Note that there is no confirmation and that all refunds are immediate and
definitive. Refunds are only supported for iDEAL, credit card, Bancontact, SOFORT Banking, PayPal, Belfius Direct Net, KBC/CBC, 
ING Home'Pay and bank transfer payments. Other types of payments cannot be refunded through our API at the moment.

```python
payment = mollie_client.payments.get(payment.id)

# Refund € 2 of this payment
refund = payment.refunds.create({
    'amount': {
        'currency': 'EUR',
        'value': '2.00'
    }
})
```

For a working example, see [Example 11 - Refund payment](https://github.com/mollie/mollie-api-python/blob/master/examples/11-refund-payment.py).

## OAuth2 ##

At https://docs.mollie.com/oauth/getting-started the OAuth process is explained. Please read this first.

OAuth authentication process redirects back to your application. Therefore you should expose your local web server (the examples) as public urls. A webservice like [ngrok.com](https://ngrok.com/) can help you with that. To run the examples, take the following steps:

1. Install the `ngrok` client (or a similar service), and make sure it works:
    - Start the Mollie oauth examples app without configuration: `python examples/oauth/oauth_app.py`
    - run `ngrok http 5000`, and visit the public URL from the ngrok client.
    - You should see a barebones webapp saying `Mollie OAuth examples: You need to setup OAuth first`.
    - Abort the examples app for now, but leave the ngrok client running. If you restart the ngrok client, you'll receive a new URL, and you will need to update the Mollie Redirect URI (from the next step) again.

2. Login to your Mollie account, and visit Developers -> Your Apps. Create a new application. In the `Redirect URL` field, you enter the ngrok public URL you just visited, and append `/callback` to the end of the URL. After saving the new application, you'll receive a `Client ID` and a `Client Secret`.

3. Go back to the examples app. Now that all other stuff is setup, we can run the examples with all required configuration:

```shell
export MOLLIE_CLIENT_ID=your_client_id
export MOLLIE_CLIENT_SECRET=your_client_secret
export MOLLIE_PUBLIC_URL=https://some.ngrok.url.io
python examples/oauth/oauth_app.py
```

After starting the application, visit the URL on the page to start the OAuth flow with Mollie.

The Authorize endpoint (where the URL takes you to) is the place on the Mollie website where the merchant logs in, and grants authorization to your client application. E.g. when the merchant clicks on the Connect with Mollie button, you should redirect the merchant to the Authorize endpoint.

The merchant can then grant the authorization to your client application for the scopes you have requested. This means that your application can access the merchants' data.

Mollie will then redirect the merchant back to the Redirect URI you have specified. The URI will contain some query parameters, which contains the auth token. At the page listening at the Redirect URI, you should extract that token, and use it to request a regular OAuth token.


### Initializing via OAuth2 ###

You should implement the `get_token` and `set_token` methods yourself. They should retrieve and store the OAuth token that is sent from Mollie somewhere in your application (f.i. in the database).

The token data is JSON, which is handled as a dict.

These are example methods, you should use a storage method that fits your application.

```python
def get_token():
    """
    :return: token (dict) or None
    """
    if os.path.exists('token.json'):
        with open('token.json', 'r') as file:
            return json.loads(file.read())


def set_token(token):
    """
    :param token: token (dict)
    :return: None
    """
    with open('token.json', 'w') as file:
        file.write(json.dumps(token))


mollie_client = Client()
is_authorized, authorization_url = mollie_client.setup_oauth(
    client_id,
    client_secret,
    redirect_uri,
    scope,
    get_token(),
    set_token,
)
# When "is_authorized" is False, you need to redirect the user to the authorization_url.

# After the user confirms the authorization ate the Mollie Authorize page, she is redirected back to your redirect_uri.
# The view on this uri should call setup_oauth_authorization_response(), with authorization_response as parameter.
# This is the full callback URL (string) from the request that the user made when returning from the Mollie website.

mollie_client.setup_oauth_authorization_response(authorization_response)

# The token will be stored via your `set_token` method for future use. Expired tokens will be refreshed by the client automatically.

# Now You can query the API:

mollie_client.organizations.get('me')
```

## API documentation ##
If you wish to learn more about our API, please visit the [Mollie Developer Portal](https://www.mollie.com/en/developers). API Documentation is available in English.

## Want to help us make our API client even better? ##

Want to help us make our API client even better? We take [pull requests](https://github.com/mollie/mollie-api-python/pulls?utf8=%E2%9C%93&q=is%3Apr), sure. But how would you like to contribute to a technology oriented organization? Mollie is hiring developers and system engineers. [Check out our vacancies](https://jobs.mollie.com/) or [get in touch](mailto:personeel@mollie.com).

## License ##
[BSD (Berkeley Software Distribution) License](https://opensource.org/licenses/bsd-license.php).
Copyright (c) 2014-2022, Mollie B.V.

## Support ##
Contact: [www.mollie.com](https://www.mollie.com) — info@mollie.com — +31 20 820 20 70
