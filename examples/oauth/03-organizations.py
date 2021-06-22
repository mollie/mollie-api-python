from mollie.api.error import Error


def main(client):
    try:
        body = ""

        # https://docs.mollie.com/reference/v2/organizations-api/current-organization

        body += "<h1>Get current organization</h1>"
        response = client.organizations.get("me")
        body += str(response)

        # https://docs.mollie.com/reference/v2/organizations-api/current-organization

        organisation_id = response.id

        body += "<h1>Get organization</h1>"
        response = client.organizations.get(organisation_id)
        body += str(response)

        return body

    except Error as err:
        return f"API call failed: {err}"
