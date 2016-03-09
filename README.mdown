![Mollie](https://www.mollie.nl/files/Mollie-Logo-Style-Small.png) 

# Mollie API client for Python #

Accepting [iDEAL](https://www.mollie.com/ideal/), [Bancontact/Mister Cash](https://www.mollie.com/mistercash/), [SOFORT Banking](https://www.mollie.com/sofort/), [Creditcard](https://www.mollie.com/creditcard/), [SEPA Bank transfer](https://www.mollie.com/overboeking/), [SEPA Direct debit](https://www.mollie.com/directdebit/), [Bitcoin](https://www.mollie.com/bitcoin/), [PayPal](https://www.mollie.com/paypal/), [Belfius Direct Net](https://www.mollie.com/belfiusdirectnet/) and [paysafecard](https://www.mollie.com/paysafecard/) online payments without fixed monthly costs or any punishing registration procedures. Just use the Mollie API to receive payments directly on your website or easily refund transactions to your customers.

[![PyPI version](https://badge.fury.io/py/mollie-api-python.svg)](http://badge.fury.io/py/mollie-api-python)

## Requirements ##
To use the Mollie API client, the following things are required:

+ Get yourself a free [Mollie account](https://www.mollie.nl/aanmelden). No sign up costs.
+ Create a new [Website profile](https://www.mollie.nl/beheer/account/profielen/) to generate API keys and setup your webhook.
+ Now you're ready to use the Mollie API client in test mode.
+ In order to accept payments in live mode, payment methods must be activated in your account. Follow [a few steps](https://www.mollie.nl/beheer/diensten), and let us handle the rest.
+ Mollie API client for Python has a dependency on [Requests](http://python-requests.org).

## Installation ##

By far the easiest way to install the Mollie API client is to install it with [pip](https://pip.pypa.io).

```
  pip install mollie-api-python
```

You may also git checkout or [download all the files](https://github.com/mollie/mollie-api-python/archive/master.zip), and include the Mollie API client manually.

## How to receive payments ##

To successfully receive a payment, these steps should be implemented:

1. Use the Mollie API client to create a payment with the requested amount, description and optionally, a payment method. It is important to specify a unique redirect URL where the customer is supposed to return to after the payment is completed.

2. Immediately after the payment is completed, our platform will send an asynchronous request to the configured webhook to allow the payment details to be retrieved, so you know when exactly to start processing the customer's order.

3. The customer returns, and should be satisfied to see that the order was paid and is now being processed.

## Getting started ##

Requiring the Mollie API Client.

```python
    import Mollie
```    

Initializing the Mollie API client, and setting your API key.

```python
    mollie = Mollie.API.Client()
    mollie.setApiKey('test_dHar4XY7LxsDOtmnkVtjNVWXLSlXsM')
```    

Creating a new payment.
    
```python
    payment = mollie.payments.create({
        'amount':      10.00,
        'description': 'My first API payment',
        'redirectUrl': 'http://webshop.example.org/order/12345'
    })
```
    
Retrieving a payment.

```python
    payment = mollie.payments.get(payment['id'])
    
    if payment.isPaid():
        print 'Payment received.'
```

### Fully integrated iDEAL payments ###

If you want to fully integrate iDEAL payments in your web site, some additional steps are required. First, you need to
retrieve the list of issuers (banks) that support iDEAL and have your customer pick the issuer he/she wants to use for
the payment.

Retrieve the list of issuers:

```python
    issuers = mollie.issuers.all()
```

_`issuers` will be a list of `Mollie.API.Object.Issuer` objects. Use the attribute `id` of this object in the
 API call, and the attribute `name` for displaying the issuer to your customer. For a more in-depth example, see [Example 4](https://github.com/mollie/mollie-api-python/blob/master/examples/4-ideal-payment.py)._

Create a payment with the selected issuer:

```python
	payment = mollie.payments.create({
		'amount'      : 10.00,
		'description' : 'My first API payment',
		'redirectUrl' : 'https://webshop.example.org/order/12345',
		'method' : Mollie.API.Object.Method.IDEAL,
		'issuer' : selected_issuer_id,  # e.g. 'ideal_INGBNL2A'
	})
```

_The `paymentUrl` attribute of the `payment` object will point directly to the online banking environment of the selected issuer._

### Refunding payments ###

The API also supports refunding payments. Note that there is no confirmation and that all refunds are immediate and
definitive. Refunds are only supported for iDEAL, credit card and Bank Transfer payments. Other types of payments cannot
be refunded through our API at the moment.

```python
	payment = mollie.payments.get(payment['id'])
	refund = mollie.payments.refund(payment)
```

## Examples ##

To run the examples you need to install [Flask](http://flask.pocoo.org/). Simply run:

```
    $ cd mollie-api-python
    $ pip install Flask 
    $ pip install requests 
    $ python examples/app.py
```

## License ##
[BSD (Berkeley Software Distribution) License](http://www.opensource.org/licenses/bsd-license.php).
Copyright (c) 2014, Mollie B.V.

## Support ##
Contact: [www.mollie.com](http://www.mollie.com) — info@mollie.com — +31 20-612 88 55

+ [More information about iDEAL via Mollie](https://www.mollie.com/ideal/)
+ [More information about credit card via Mollie](https://www.mollie.com/creditcard/)
+ [More information about Bancontact/Mister Cash via Mollie](https://www.mollie.com/mistercash/)
+ [More information about SOFORT Banking via Mollie](https://www.mollie.com/sofort/)
+ [More information about SEPA Bank transfer via Mollie](https://www.mollie.com/banktransfer/)
+ [More information about SEPA Direct debit via Mollie](https://www.mollie.com/directdebit/)
+ [More information about Bitcoin via Mollie](https://www.mollie.com/bitcoin/)
+ [More information about PayPal via Mollie](https://www.mollie.com/paypal/)
+ [More information about Belfius Direct Net via Mollie](https://www.mollie.com/belfiusdirectnet/)
+ [More information about paysafecard via Mollie](https://www.mollie.com/paysafecard/)

![Powered By Mollie](https://www.mollie.nl/images/badge-betaling-medium.png)
