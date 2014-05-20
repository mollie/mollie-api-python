#
# Example 3 - How to show a return page to the customer.
#
# In this example we retrieve the order stored in the database.
# Here, it's unnecessary to use the Mollie API Client.
#
import flask
from app import database_read


def main():
    if 'order_nr' not in flask.request.args:
        flask.abort(404, 'Unknown order_nr')

    body = "<p>Your payment status is '%s'" % database_read(flask.request.args['order_nr'])
    body += '<p>'
    body += '<a href="/">Back to examples</a><br>'
    body += '</p>'

    return body


if __name__ == '__main__':
    print main()