import os

import flask

app = flask.Flask(__name__)
examples = [
    '1-new-payment',
    '2-webhook-verification',
    '3-return-page',
    '4-ideal-payment',
    '5-payments-history',
    '6-list-activated-methods',
    '7-new-customer',
    '8-list-customers',
    '9-create-customer-payment',
    '10-customer-payment-history',
    '11-refund-payment',
]


@app.route('/')
def show_list():
    body = ''
    for example in examples:
        body += '<a href="/{example}">{example}</a><br>'.format(example=example)
    return body


@app.route('/<example>', methods=['GET', 'POST'])
def run_example(example=None):
    if example not in examples:
        flask.abort(404, 'Example does not exist')
    return __import__(example).main()


if __name__ == "__main__":
    app.debug = True
    app.run()

#
# NOTE: This example uses a plain txt file as a "database". Please use a real database like MySQL in production.
#


def database_write(order_nr, status):
    order_nr = int(order_nr)
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'orders', 'order-{nr}.txt'.format(nr=order_nr))
    database = open(file, 'w')
    database.write(status)


def database_read(order_nr):
    order_nr = int(order_nr)
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'orders', 'order-{nr}.txt'.format(nr=order_nr))
    database = open(file, 'r')
    return database.read()
