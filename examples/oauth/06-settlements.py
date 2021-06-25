from mollie.api.error import Error


def main(client):
    try:
        body = ""

        # https://docs.mollie.com/reference/v2/settlements-api/list-settlements

        body += "<h1>List settlements</h1>"
        response = client.settlements.list()
        body += str(response)

        settlement_id = next(response).id

        # https://docs.mollie.com/reference/v2/settlements-api/get-settlement

        body += "<h1>Get settlement</h1>"
        response = client.settlements.get(settlement_id)
        body += str(response)

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
        response = client.settlement_payments.with_parent_id(settlement_id).list()
        body += str(response)

        # https://docs.mollie.com/reference/v2/settlements-api/list-settlement-refunds

        body += "<h1>List settlement refunds</h1>"
        response = client.settlement_refunds.with_parent_id(settlement_id).list()
        body += str(response)

        # https://docs.mollie.com/reference/v2/settlements-api/list-settlement-chargebacks

        body += "<h1>List settlement chargebacks</h1>"
        response = client.settlement_chargebacks.with_parent_id(settlement_id).list()
        body += str(response)

        # https://docs.mollie.com/reference/v2/settlements-api/list-settlement-captures

        body += "<h1>List settlement captures</h1>"
        settlement = client.settlements.get(settlement_id)
        response = client.settlement_captures.on(settlement).list()
        body += str(response)

        return body

    except Error as err:
        return f"API call failed: {err}"
