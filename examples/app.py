import json
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
    '12-new-order',
    '13-handle-order-status-change',
    '14-cancel-order',
    '15-list-orders',
    '16-cancel-order-line',
    '17-order-return-page',
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


def database_write(my_webshop_id, data):
    my_webshop_id = int(my_webshop_id)
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'orders', 'order-{nr}.txt'.format(nr=my_webshop_id))
    database = open(file, 'w')
    database.write(json.dumps(data))


def database_read(my_webshop_id):
    my_webshop_id = int(my_webshop_id)
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'orders', 'order-{nr}.txt'.format(nr=my_webshop_id))
    database = open(file, 'r')
    return json.loads(database.read())
