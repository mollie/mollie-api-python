# Refactoring the Mollie Client API to be more logical

This document describes the changes in the way certain endpoint paths are exposed to the developer by the Mollie Python API client. Part of the existing API in the `v2` library is remnant of the `v1` code that we inherited. Other parts were newly added over time, many of them due to lack for a better way to add the functionality, given the existing architecture. With these changes put into place, the client API will be much clearer, but lots of things will move around. In some situations, a proper deprecation path is not really possible. 

This warrants a major version change (i.e. we are releasing the changes as `v3.0`).

## Table of contents

 * [Problems with the v2 client API](#problems-with-the-v2-client-api)
 * [Refactoring](#refactoring)
 * [Overview of all documented API calls](#overview-of-all-documented-api-calls)
 * [Other changes](#other-changes)

## Problems with the v2 client API

Some issues that were popping up during Client API development, or during implementation of the client API in applications:

- Many endpoint handlers have methods that aren't supported by the API. E.g. A method exists at `client.refunds.get()`, but the method doesn't work, since it only results in actual data when you do `client.refunds.with_parent_id(:payment_id).get(:refund_id)`. Under the hood, this uses the same `.get()` method as the first example, but due to the wrong context the method doesn't work sometimes. Exposing the `.get()` method only in the correct context will make things much simpler.
- Some methods are somewhat bolted on, which means that they aren't easy to find. At the more logical path (where you'd expect the functionality to live), there is nothing, or something that doesn't work. E.g. To create an order refund, you currently need to do `order = client.orders.get(:order_id); order.create_refund(:data)`. The `order` object also has an `order.refunds` property, but that is the 'List order refunds' functionality, and it has no support for creating refunds.
- Some methods have unexpected signatures, which means that they are hard to use. E.g. Throughout the API we expose a method `.with_parent_id(:parent_id)` which takes a single argument. But in order to list subscription payments, you need to use `client.subscription_payments.with_parent_id(:customer_id, :subscription_id).list()`, with `with_parent_id()` taking 2 required arguments.
- Some methods perform unexpected API calls. E.g. The current `order.refunds` property performs an API call to list the Order refunds, but that is not clear since, in general, we do listings using the `.list()` method. So `order.refunds.list()` would be much clearer. This also makes room in the API for adding the `order.refunds.create()` method.


## Refactoring

To make all the above much cleaner, we have done a few things:

- Expose the explicit methods that retrieve data from the API only on logical places in the API. The Refunds API has several endpoints that handle data only in the context of a Payment. We should expose those methods only on a Payment object, and no longer on various objects directly on the Client object, which use methods like `.with_parent_id(:parent_id)` to inject details about a parent Payment that is never created.
- Remove the methods that revolve around injecting details about a parent object that is not actually created: `.with_parent_id()` and `.on()`. Given the changes from the previous point (the parent is the actual place where the functionality is exposed), these methods are no longer useful.
- Update some object properties that currently expose partial functionality, and replace them with generic resource handlers that expose all the available API methods. This means refactoring the `payment.refunds` property into an object that exposes a `.list()`, a `.get()`, a `.delete()` and a `.create()` method.


# Overview of all documented API calls

The list below corresponds with the Mollie API documentation. It shows all currently documented Mollie API endpoints, with the old and new code to perform the correct API call.

## Payments API

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| Create payment | `client.payments.create(:data)` | `client.payments.create(:data)` | No changes |
| Get payment | `client.payments.get(:payment_id)` |  `client.payments.get(:payment_id)` | No changes |
| Update payment | `client.payments.update(:payment_id, :data)` | `client.payments.update(:payment_id, :data)` | No changes |
| Cancel payment | `client.payments.delete(:payment_id)` | `client.payments.delete(:payment_id)` | No changes |
| List payments | `client.payments.list()` | `client.payments.list()` | No changes |


## Methods API

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| List payment methods | `client.methods.list()` | `client.methods.list()` | No changes |
| List all payment methods | `client.methods.all()` | `client.methods.all()` | No changes |
| Get payment method | `client.methods.get(:method_id)` | `client.methods.get(:method_id)` | No changes |


## Refunds API

- Various existing codepaths are removed: `client.payment_refunds`, `order.create_refund()`.
- The `order.refunds` and `payment.refunds` objects still exist but are working differently.

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| Create payment refund | `client.payment_refunds.with_parent_id(:payment_id).create(:data)` | `payment = client.payments.get(:payment_id); payment.refunds.create(:data)` ||
| Get payment refund | `client.payment_refunds.with_parent_id(:payment_id).get(:id)` | `payment = client.payments.get(:payment_id); payment.refunds.get(:id)` ||
| Cancel payment refund | `client.payment_refunds.with_parent_id(:payment_id).delete(:id)` | `payment = client.payments.get(:payment_id); payment.refunds.delete(:id)` ||
| List payment refunds | `client.payment_refunds.with_parent_id(:payment_id).list()` <br>OR<br> `payment = client.payments.get(:payment_id); payment.refunds` | `payment = client.payments.get(:payment_id); payment.refunds.list()` ||
| Create order refund | `order = client.orders.get(:order_id); order.create_refund(:data)` | `order = client.orders.get(:order_id); order.refunds.create(:data)` ||
| List order refunds | `order = client.orders.get(:order_id); order.refunds` | `order = client.orders.get(:order_id); order.refunds.list()` ||
| List refunds | `client.refunds.list()` | `client.refunds.list()` | No changes |


## Chargebacks API 

- The `client.payment_chargebacks` object is removed.
- The `payment.chargebacks` object still exists, but is working differently.

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| Get payment chargeback | `client.payment_chargebacks.with_parent_id(:payment_id).get(:chargeback_id)` | `payment = client.payments.get(:payment_id); payment.chargebacks.get(:chargeback_id)` ||
| List payment chargebacks | `client.payment_chargebacks.with_parent_id(:payment_id).list()` <br>OR<br> `payment = client.payments.get(:payment_id); payment.chargebacks` | `payment = client.payments.get(:payment_id); payment.chargebacks.list()` ||
| List chargebacks | `client.chargebacks.list()` | `client.chargebacks.list()` | No changes |


## Captures API

- The `client.captures` object is removed.
- The `payment.captures` object still exists, but is working differently.

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| Get capture | `client.captures.with_parent_id(:payment_id).get(:capture_id)` | `payment = client.payments.get(:payment_id); payment.captures.get(:capture_id)` ||
| List captures | `client.captures.with_parent_id(:payment_id).list()` <br>OR<br> `payment = client.payments.get(:payment_id); payment.captures` | `payment = client.payments.get(:payment_id); payment.captures.list()` ||


## Payment links API

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| Create payment link | `client.payment_links.create(:data)` | `client.payment_links.create(:data)` | No changes |
| Get payment link | `client.payment_links.get(:payment_link_id)` | `client.payment_links.get(:payment_link_id)` | No changes |
| List payment links | `client.payment_links.list()` | `client.payment_links.list()` | No changes |


## Orders API

- The `order.update_line()`, `order.cancel_lines()` and `order.create_payment()` methods are removed.
- The `order.lines` and `order.payments` objects still exist but are working differently.

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| Create order | `client.orders.create(:data)` | `client.orders.create(:data)` | No changes |
| Get order | `client.orders.get(:order_id)` | `client.order.get(:order_id)` | No changes |
| Update order | `client.order.update(:order_id, :data)` | `client.order.update(:order_id, :data)` | No changes |
| Cancel order | `client.order.delete(:order_id)` | `client.order.delete(:order_id)` | No changes |
| List orders | `client.order.list()` | `client.order.list()` | No changes |
| Update order line | `order = client.orders.get(:order_id); order.update_line(:line_id, :data)` | `order = client.orders.get(:order_id); order.lines.update(:line_id, :data)` ||
| Cancel order lines | `order = client.orders.get(:order_id); order.cancel_lines(:data)` | `order = client.orders.get(:order_id); order.lines.delete_lines(:data)` <br>OR<br> `order = client.orders.get(:order_id); order.lines.delete(:line_id)` ||
| Create order payment | `order = client.orders.get(:order_id); order.create_payment(:data)` | `order = client.orders.get(:order_id); order.payments.create(:data)` ||


## Shipments API

- The `client.shipments` object and the `order.create_shipment()`, `order.get_shipment()`, `order.update_shipment()` methods are removed.
- The `order.shipments` object still exists, but is working differently.

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| Create shipment | `order = client.orders.get(:order_id); order.create_shipment(:data)` | `order = client.orders.get(:order_id); order.shipments.create(:data)` ||
| Get shipment | `order = client.orders.get(:order_id); order.get_shipment(:shipment_id)` | `order = client.orders.get(:order_id); order.shipments.get(:shipment_id)` ||
| Update shipment | `order = client.orders.get(:order_id); order.update_shipment(:shipment_id, :data)` | `order = client.orders.get(:order_id); order.shipments.update(:shipment_id¸ :data)` ||
| List shipments | `order = client.orders.get(:order_id); order.shipments` | `order = client.orders.get(:order_id); order.shipments.list()` ||


## Customers API

- The `client.customer_payments` object is removed.
- The `customer.payments` object still exists but is working differently.

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| Create customer | `client.customers.create(:data)` | `client.customers.create(:data)` | No changes |
| Get customer | `client.customers.get(:customer_id)` | `client.customers.get(:customer_id)` | No changes |
| Update customer | `client.customers.update(:customer_id, :data)` | `client.customers.update(:customer_id, :data)` | No changes |
| Delete customer | `client.customers.delete(:customer_id)` | `client.customers.delete(:customer_id)` | No changes |
| List customers | `client.customers.list()` | `client.customers.list()` | No changes |
| Create customer payment | `client.customer_payments.with_parent_id(:customer.id).create(:data)` | `customer = client.customers.get(:customer_id); customer.payments.create(:data)` ||
| List customer payments | `customer = client.customers.get(:customer_id); customer.payments` <br>OR<br> `client.customer_payments.with_parent_id(:customer_id).list()` | `customer = client.customers.get(:customer_id); customer.payments.list()` ||


## Mandates API

- The `client.customer_mandates` object is removed.
- The `customer.mandates` object still exists but is working differently.

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| Create mandate | `client.customer_mandates.on(:customer_id).create(:data)` | `customer = client.customers.get(:customer_id); customer.mandates.create(:data)` ||
| Get mandate | `client.customer_mandates.on(:customer_id).get(:mandate_id)` <br>OR<br> `payment = client.payments.get(:payments.id); payment.mandate` | `customer = client.customers.get(:customer_id); customer.mandates.get(:mandate_id)` ||
| Revoke mandate | `client.customer_mandates.on(:customer_id).delete(:mandate_id)` | `customer = client.customers.get(:customer_id); customer.mandates.delete(:mandate_id)` ||
| List mandates | `customer = client.customers.get(:customer_id); customer.mandates` <br>OR<br> `client.customer_mandates.with_parent_id(:customer_id).list()` | `customer = client.customers.get(:customer_id); customer.mandates.list()` ||


## Subscriptions API

- The `client.subscription_payments` object is removed.
- The totally unexpected call to `client.subscription_payments.with_parent_id(:customer_id, :subscription_id)` with 2 arguments will be removed.
- The `customer.subscriptions` object still exists but is working differently.

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| Create subscription | `client.customer_subscriptions.with_parent_id(:customer_id).create(:data)` | `customer = client.customers.get:customer_id); customer.subscriptions.create(:data)` ||
| Get subscription | `client.customer_subscriptions.with_parent_id(:customer_id).get(:subscription_id)` <br>OR<br> `payment = client.payments.get(:payment_id); payment.subscription` | `customer = client.customers.get:customer_id); customer.subscriptions.get(:subscription_id)` ||
| Update subscription | `client.customer_subscriptions.with_parent_id(:customer_id).update(:subscription_id, :data)` | `customer = client.customers.get:customer_id); customer.subscriptions.update(:subscription_id, :data)` ||
| Cancel subscription | `client.customer_subscriptions.with_parent_id(:customer_id).delete(:subscription_id)` | `customer = client.customers.get:customer_id); customer.subscriptions.delete(:subscription_id)` ||
| List subscriptions | `client.customer_subscriptions.with_parent_id(:customer_id).list()` <br>OR<br> `customer = client.customers.get:customer_id); customer.subscriptions` | `customer = client.customers.get(:customer_id); customer.subscriptions.list()` ||
| List all subscriptions | `client.subscriptions.list()` | `client.subscriptions.list()` | No changes |
| List subscription payments | `client.subscription_payments.with_parent_id(:customer_id, :subscription_id).list()` | `customer = client.customers.get(:customer_id); subscription = customer.subscriptions.get(:subscription_id); payments = subscription.payments.list()` ||


## OAuth API

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| Authorize | `client.setup_oauth()` | `client.setup_oauth()` | Used internally, no changes |
| Generate tokens | `client.setup_oauth_authorization_response()` | `client.setup_oauth_authorization_response()` | Used internally, no changes |
| Revoke token | Not implemented | TODO | This will be implemented later |


## Permissions API

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| Get permission | `client.permissions.get(:permission_id)` | `client.permissions.get(:permission_id)` | No changes |
| List permissions | `client.permissions.list()` | `client.permissions.list()` | No changes |


## Organizations API

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| Get current organization | `client.organizations.get("me")` | `client.organizations.get("me")` | No changes |
| Get organization | `client.organizations.get(:organization_id)` | `client.organizations.get(:organization_id)` | No changes |
| Get partner status | Not implemented | TODO | This will be implemented later |


## Profiles API

- The `client.profile_methods` object is removed.
- The totally unexpected call to `client.profile_methods.with_parent_id(:profile_id, :method_id)` with 2 arguments will be removed.

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| Create profile | `client.profiles.create(:data)` | `client.profiles.create(:data)` | No changes |
| Get profile | `client.profiles.get(:profile_id)` | `client.profiles.get(:profile_id)` | No changes |
| Get current profile | `client.profiles.get("me")` | `client.profiles.get("me")` | No changes |
| Update profile | `client.profiles.update(:profile_id, :data)` | `client.profiles.update(:profile_id, :data)` | No changes |
| Delete profile | `client.profiles.delete(:profile_id)` | `client.profiles.delete(:profile_id)` | No changes |
| List profiles | `client.profiles.list()` | `client.profiles.list()` | No changes |
| Enable payment method | `client.profile_methods.with_parent_id(:profile_id, :method_id).create()` | `profile = client.profiles.get(:profile_id); profile.methods.enable(:method_id)` ||
| Disable payment method | `client.profile_methods.with_parent_id(:profile_id, :method_id).delete()` | `profile = client.profiles.get(:profile_id); profile.methods.disable(:method_id)` ||
| Enable gift card issuer | `client.profile_methods.with_parent_id(:profile_id, "giftcard").create(:issuer_id)` | `profile = client.profiles.get(:profile_id); profile.methods.enable_issuer("giftcard", :issuer_id)` ||
| Disable gift card issuer | `client.profile_methods.with_parent_id(:profile_id, "giftcard").delete(:issuer_id)` | `profile = client.profiles.get(:profile_id); profile.methods.disable_issuer("giftcard", :issuer_id)` ||
| Enable voucher issuer | `client.profile_methods.with_parent_id(:profile_id, "voucher").create(:issuer_id)` | `profile = client.profiles.get(:profile_id); profile.methods.enable_issuer("voucher", :issuer_id, :data)` ||
| Disable voucher issuer | `client.profile_methods.with_parent_id(:profile_id, "voucher").delete(:issuer_id)` | `profile = client.profiles.get(:profile_id); profile.methods.disable_issuer("voucher", :issuer_id)` ||

There is also some profile-related functionality that has been updated with does not relate directly to a documented Profiles API endpoint.

- The `client.profile_payments`, `client.profile_refunds` and `client.profile_chargebacks` objects are removed.
- The `profile.methods`, `profile.chargebacks`, `profile.payments` and `profile.refunds` objects still exist, but they are working differently.

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| List profile payments | `client.profile_payments.with_parent_id(:profile_id).list()` <br>OR<br> `profile = client.profiles.get(:profile_id); profile.payments` | `profile = client.profiles.get(:profile_id); profile.payments.list()` | Same result can be achieved using `client.payments.list(profileId=:profile_id)` in old and new client |
| List profile refunds | `client.profile_refunds.with_parent_id(:profile_id).list()` <br>OR<br> `profile = client.profiles.get(:profile_id); profile.refunds` | `profile = client.profiles.get(:profile_id); profile.refunds.list()` | Same result can be achieved using `client.refunds.list(profileId=:profile_id)` in old and new client |
| List profile chargebacks | `client.profile_chargebacks.with_parent_id(:profile_id).list()` <br>OR<br> `profile = client.profiles.get(:profile_id); profile.chargebacks` | `profile = client.profiles.get(:profile_id); profile.chargebacks.list()` | Same result can be achieved using `client.chargebacks.list(profileId=:profile_id)` in old and new client |
| List profile methods | `client.profile_methods.with_parent_id(:profile_id).list()` <br>OR<br> `profile = client.profiles.get(:profile_id); profile.methods` | `profile = client.profiles.get(:profile_id); profile.methods.list()` | Same result can be achieved using `client.methods.list(profileId=:profile_id)` in old and new client |



## Onboarding API

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| Submit onboarding data | `client.onboarding.create("me", :data)` | `client.onboarding.create(:data)` ||
| Get onboarding status | `client.onboarding.get("me")` |`client.onboarding.get("me")` | No changes |


## Balances API

The Balances API is not supported yet in any client.


## Settlements API

- The `client.settlement_payments`, `client.settlement_refunds` `client.settlement_chargebacks`, and `client.settlement_captures` objects are removed.
- The `settlement.payments`, `settlement.refunds`, `settlement.chargebacks` and `settlement.captures` objects still exist, but they are working differently.

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| Get settlement | `client.settlements.get(:settlement_id)` | `client.settlements.get(:settlement_id)` | No changes |
| Get next settlement | `client.settlements.get("next")` | `client.settlements.get("next")` | No changes |
| Get open settlement | `client.settlements.get("open")` | `client.settlements.get("open")` | No changes |
| List settlements | `client.settlements.list()` | `client.settlements.list` | No changes |
| List settlement payments | `client.settlement_payments.with_parent_id(:settlement_id).list()` | `client.settlements.get(:settlement_id); settlement.payments.list()` ||
| List settlement captures | `client.settlement_captures.with_parent_id(:settlement_id).list()` | `settlement = client.settlements.get(); settlement.captures.list()` ||
| List settlement refunds | `client.settlement_refunds.with_parent_id(:settlement_id).list()` | `settlement = client.settlements.get(); settlement.refunds.list()` ||
| List settlement chargebacks | `client.settlement_chargebacks.with_parent_id(:settlement_id).list()` | `settlement = client.settlements.get(); settlement.chargebacks.list()` ||


## Invoices API

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| Get invoice | `client.invoices.get(:invoice_id)` | `client.invoices.get(:invoice_id)` | No changes |
| List invoices | `client.invoices.list()` | `client.invoices.list()` | No changes |


## Clients API

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| Get client | `client.clients.get(:client_id)` | `client.clients.get(:client_id)` | No changes |
| List clients | `client.clients.list()` | `client.clients.list()` | No changes |


# Other changes

## Properties should not perform heavy operations

In general, object properties are seen by developers as lightweight data accessors. They are supposed to be 'cheap'. In the `v2` codebase, several object properties actually performed API calls. Some of them are already addressed above, f.i. `Payment.refunds`, which has changed into `Payment.refunds.list()`. There are also other properties, which mainly returned single result objects, that not directly represent an API endpoint like the methods above. They are, for instance, based on the existance of a property in the `_links` section of an API response, like `Refund.payment`: the payment related to a refund. 

In `v3`, all result object properties that perform API calls have been replaced with regular methods. Below you'll find a list of all of these properties, and the methods that have replaced them.


| 2.x client property | New client method |
|---------------------|-------------------|
| `Capture.payment` | `Capture.get_payment()` |
| `Capture.shipment` | `Capture.get_shipment()` |
| `Capture.settlement` | `Capture.get_settlement()` |
| `Chargeback.payment` | `Chargeback.get_payment()` |
| `Chargeback.settlement` | `Chargeback.get_settlement()` |
| `Client.organization` | `Client.get_organization()` |
| `Client.onboarding` | `Client.get_onboarding()` |
| `Mandate.customer` | `Client.get_customer()` |
| `Onboarding.organization` | `Onboarding.get_organization()` |
| `Payment.settlement` | `Payment.get_settlement()` |
| `Payment.mandate` | `Payment.get_mandate()` |
| `Payment.subscription` | `Payment.get_subscription()` |
| `Payment.customer` | `Payment.get_customer()` |
| `Payment.order` | `Payment.get_order()` |
| `Refund.payment` | `Refund.get_payment()` |
| `Refund.settlement` | `Refund.get_settlement()` |
| `Refund.order` | `Refund.get_order()` |
| `Settlement.invoice` | `Settlement.get_invoice()` |
| `Shipment.order` | `Shipment.get_order()` |
| `Subscription.customer` | `Subscription.get_customer()` |
| `Subscription.profile` | `Subscription.get_profile()` |
| `Subscription.mandate` | `Subscription.get_mandate()` |
