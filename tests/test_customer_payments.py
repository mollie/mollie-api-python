from mollie.api.objects.payment import Payment

from .utils import assert_list_object

CUSTOMER_ID = "cst_8wmqcHMN4U"


def test_list_customer_payments(client, response):
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/payments", "customer_payments_multiple")

    customer = client.customers.get(CUSTOMER_ID)
    payments = customer.payments.list()
    assert_list_object(payments, Payment)


def test_create_customer_payment(client, response):
    response.get(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}", "customer_single")
    response.post(f"https://api.mollie.com/v2/customers/{CUSTOMER_ID}/payments", "payment_single")

    customer = client.customers.get(CUSTOMER_ID)
    payment = customer.payments.create(
        {
            "amount": {"currency": "EUR", "value": "10.00"},
            "description": "Order #12345",
            "redirectUrl": "https://webshop.example.org/order/12345/",
            "webhookUrl": "https://webshop.example.org/payments/webhook/",
            "method": "ideal",
        }
    )
    assert isinstance(payment, Payment)
    assert payment.customer_id == CUSTOMER_ID
