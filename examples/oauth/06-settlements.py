# coding=utf-8

from __future__ import print_function

from mollie.api.error import Error


def main(client):
    try:

        body = ''

        # https://docs.mollie.com/reference/v2/settlements-api/get-settlement

        body += '<h1>Get settlement</h1>'
        response = client.settlement.get()

        print(response)
        body += str(response)

        # https://docs.mollie.com/reference/v2/settlements-api/get-next-settlement

        body += '<h1>Get next settlement</h1>'
        response = client.settlement.next()

        print(response)
        body += str(response)

        # https://docs.mollie.com/reference/v2/settlements-api/get-open-settlement

        body += '<h1>Get open settlement</h1>'
        response = client.settlement.open()

        print(response)
        body += str(response)

        # https://docs.mollie.com/reference/v2/settlements-api/list-settlements

        body += '<h1>List settlements</h1>'
        response = client.settlement.list()

        print(response)
        body += str(response)

        # https://docs.mollie.com/reference/v2/settlements-api/list-settlement-payments

        body += '<h1>List settlement payments</h1>'
        response = client.settlement.payments.list()

        print(response)
        body += str(response)

        # https://docs.mollie.com/reference/v2/settlements-api/list-settlement-refunds

        body += '<h1>List settlement refunds</h1>'
        response = client.settlement.refunds()

        print(response)
        body += str(response)

        # https://docs.mollie.com/reference/v2/settlements-api/list-settlement-chargebacks

        body += '<h1>List settlement chargebacks</h1>'
        response = client.settlement.chargebacks()

        print(response)
        body += str(response)

        # https://docs.mollie.com/reference/v2/settlements-api/list-settlement-captures

        body += '<h1>List settlement captures</h1>'
        response = client.settlement.captures()

        print(response)
        body += str(response)

        return body

    except Error as err:
        return 'API call failed: {error}'.format(error=err)
