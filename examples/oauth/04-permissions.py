from mollie.api.error import Error


def main(client):
    try:

        # https://docs.mollie.com/reference/v2/permissions-api/list-permissions

        body = "<h1>List permissions</h1>"
        response = client.permissions.list()
        body += str(response)

        # https://docs.mollie.com/reference/v2/permissions-api/get-permission

        body += "<h1>Get permission</h1>"
        response = client.permissions.get("payments.read")
        body += str(response)

        return body

    except Error as err:
        return f"API call failed: {err}"
