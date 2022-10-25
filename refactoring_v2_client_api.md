# Refactoring the Client API to be more logical.

This document describes the changes in the way certain endpoint paths are exposed to the developer by the Mollie Python API client. Part of the existing API is remnant of the `v1` client that was inherited. Other parts were newly added over time, many of them due to lack for a better way to add the functionality, given the existing architecture.

When the proposed changes are put into place, the client API will be much clearer, but lots of things will move around. In some situations, a proper deprecation path will not really be possible. This would warrant a major version change (i.e. release as `v3.0`).

## Problems with the v2 client API

Some issues that are popping up during Client API development, or during implementation of the client API in applications:

- Many endpoint handlers have methods that aren't supported by the API. E.g. A method exists at `client.refunds.get()`, but the method doesn't work, since it only results in actual data when you do `client.refunds.with_parent_id(:payment_id).get(:refund_id)`. Exposing the `.get()` method only in the correct context will make things much simpler.
- Some methods are somewhat bolted on, which means that they aren't easy to find. At the more logical path (where you'd expect the functionality to live), there is nothing, or something that doesn't work. E.g. To create an order refund, you currently need to do `order = client.orders.get(:order_id); order.create_refund(:data)`. The `order` object also has an `order.refunds` property, but that is the 'List order refunds' functionality, and it has no support for creating refunds.
- Some methods have unexpected signatures, which means that they are hard to use. E.g. Throughout the API we expose a method `.with_parent_id(:parent_id)` which takes a single argument. But in order to list subscription payments, you need to use `client.subscription_payments.with_parent_id(:customer_id, :subscription_id).list()`, with `with_parent_id()` taking 2 required arguments.
- Some methods perform unexpected API calls. E.g. The current `order.refunds` property performs an API call to list the Order refunds, but that is not clear since, in general, we do listings using the `.list()` method. So `order.refunds.list()` would be much clearer. This also makes room in the API for adding the `order.refunds.create()`.

## Refactoring

To make all the above much cleaner, we would have to do a few things:

- Expose the explicit methods that retrieve data from the API only on logical places in the API. The Refunds API has several endpoints that handle data in the context of a Payment. We should expose those methods only on a Payment object, and no longer on various objects directly on the Client object, which use methods like `.with_parent_id(:parent_id)` to inject details about a parent that is never created.
- Remove some methods that revolve around injecting details about a parent object that is not actually created: `.with_parent_id()` and `.on()`. Given the changes from the previous point (the parent is the actual place where the functionality is exposed), these methods are no longer useful.
- Update some object properties that currently expose partial functionality, and replace them with generic resource handlers that expose all the available API methods. This means refactoring the `payment.refunds` property into an object that exposes a `.list()`, a `.get()`, a `.delete()` and a `.create()` method.

All of the above should be applied throughout the whole library.


# Overview of all documented API calls.

The list below corresponds with the Mollie API documentation.

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
- The `order.refunds` and `payment.refunds` object still exist but are working differently.

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
| List chargebacks | `client.chargeback.list()` | `client.chargeback.list()` | No changes |


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


## Subscriptions API

- The `client.subscription_payments` object is removed.
- The totally unexpected call to `client.subscription_payments.with_parent_id(:customer_id, :subscription_id)` with 2 arguments will be removed.
- The `customer.subscriptions` object still exists but is working differently.

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| List subscriptions | `client.customer_subscriptions.with_parent_id(:customer_id).list()` <br>OR<br> `customer = client.customers.get:customer_id); customer.subscriptions` | `customer = client.customers.get(:customer_id); customer.subscriptions.list()` ||
| List subscription payments | `client.subscription_payments.with_parent_id(:customer_id, :subscription_id).list()` | `customer = client.customers.get(:customer_id); subscription = customer.subscriptions.get(:subscription_id); payments = subscription.payments.list()` ||


### Settlements API

- The `client.settlement_refunds` and `client.settlement_captures` objects are removed.
- The `settlement.refunds` and `settlement.captures` objects still exist, but they are working differently.

| Description | 2.x client path | New client path | Notes |
| ------------|-----------------|-----------------|-------|
| List settlement refunds | `client.settlement_refunds.with_parent_id(:settlement_id).list()` | `settlement = client.settlements.get(); settlement.refunds.list()` ||
| List settlement captures | `client.settlement_captures.with_parent_id(:settlement_id).list()` | `settlement = client.settlements.get(); settlement.captures.list()` ||

## Proposed solution

- We will refactor the library and example code to use the interface described above.
- We will provide a document describing all old and new uses of the Client API, like the example listings above. This will make it easier for users to update their code.
- We release the new code with a major version bump (from 2.x to 3.0), with clear Release notes, so everybody will be aware of the changes.
