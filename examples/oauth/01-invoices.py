from mollie.api.error import Error

INVOICE_ID = "inv_xBEbP9rvAq"


def main(client):
    try:

        # https://docs.mollie.com/reference/v2/invoices-api/list-invoices

        body = "<h1>List invoices</h1>"
        body += "<ul>"
        for invoice in client.invoices.list(limit=10):
            body += f"<li>{invoice.id}: {invoice.net_amount}<a href='{invoice.pdf}'>Download PDF</a></li>"
        body += "</ul>"

        # https://docs.mollie.com/reference/v2/invoices-api/get-invoice

        # body += '<h1>Get invoice</h1>'
        # body += str(client.invoices.get(INVOICE_ID))

        return body

    except Error as err:
        return f"API call failed: {err}"
