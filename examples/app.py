import json
import os

import flask

app = flask.Flask(__name__)
examples = [
    '01-new-payment',
    '02-webhook-verification',
    '03-return-page',
    '04-ideal-payment',
    '05-payments-history',
    '06-list-activated-methods',
    '07-new-customer',
    '08-list-customers',
    '09-create-customer-payment',
    '10-customer-payment-history',
    '11-refund-payment',
    '12-new-order',
    '13-order-webhook-verification',
    '14-cancel-order',
    '15-list-orders',
    '16-cancel-order-line',
    '17-order-return-page',
    '18-ship-order-completely',
    '19-ship-order-partially',
    '20-get-shipment',
    '21-list-order-shipments',
    '22-refund-order-completely',
    '23-update-shipment-tracking',
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
# NOTE: This example uses json files as a "database".
# Please use a real database like MySQL in production.
#


def database_write(my_webshop_id, data):
    my_webshop_id = int(my_webshop_id)
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'orders',
                        'order-{nr}.json'.format(nr=my_webshop_id))
    database = open(file, 'w')
    database.write(json.dumps(data))


def database_read(my_webshop_id):
    my_webshop_id = int(my_webshop_id)
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'orders',
                        'order-{nr}.json'.format(nr=my_webshop_id))
    database = open(file, 'r')
    return json.loads(database.read())
