from mollie.api.error import Error


def main(client):
    try:
        body = ""

        # https://docs.mollie.com/reference/v2/settlements-api/list-settlements

        body += "<h1>List settlements</h1>"
        settlements = client.settlements.list()
        body += str(settlements)

        settlement_id = next(settlements).id

        # https://docs.mollie.com/reference/v2/settlements-api/get-settlement

        body += "<h1>Get settlement</h1>"
        settlement = client.settlements.get(settlement_id)
        body += str(settlement)

        # https://docs.mollie.com/reference/v2/settlements-api/get-next-settlement

        body += "<h1>Get next settlement</h1>"
        response = client.settlements.get("next")
        body += str(response)

        # https://docs.mollie.com/reference/v2/settlements-api/get-open-settlement

        body += "<h1>Get open settlement</h1>"
        response = client.settlements.get("open")
        body += str(response)

        # https://docs.mollie.com/reference/v2/settlements-api/list-settlement-payments

        body += "<h1>List settlement payments</h1>"
        response = settlement.payments.list()
        body += str(response)

        # https://docs.mollie.com/reference/v2/settlements-api/list-settlement-refunds

        body += "<h1>List settlement refunds</h1>"
        response = settlement.refunds.list()
        body += str(response)

        # https://docs.mollie.com/reference/v2/settlements-api/list-settlement-chargebacks

        body += "<h1>List settlement chargebacks</h1>"
        response = settlement.chargebacks.list()
        body += str(response)

        # https://docs.mollie.com/reference/v2/settlements-api/list-settlement-captures

        body += "<h1>List settlement captures</h1>"
        response = settlement.captures.list()
        body += str(response)

        return body

    except Error as err:
        return f"API call failed: {err}"
