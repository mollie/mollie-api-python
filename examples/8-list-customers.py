# coding=utf-8
#
# Example 8 - Retrieving all of your customers with offset and count
#
from __future__ import print_function

import os

from mollie.api.client import Client
from mollie.api.error import Error


def main():
    try:
        #
        # Initialize the Mollie API library with your API key.
        #
        # See: https://www.mollie.com/dashboard/settings/profiles
        #
        api_key = os.environ.get('MOLLIE_API_KEY', 'test_test')
        mollie_client = Client()
        mollie_client.set_api_key(api_key)

        amount_of_customers_to_retrieve = 20
        params = {
            'limit': amount_of_customers_to_retrieve,
        }

        #
        # Get the latest 20 customers
        #
        # See: https://www.mollie.com/nl/docs/reference/customers/list
        #
        customers = mollie_client.customers.all(**params)

        body = '<p>Showing the last %s customers for your API key.</p>' % customers.count

        if int(customers.count) == 0:
            return body

        body += """
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Payment creation</th>
                        <th>Payment History</th>
                    </tr>
                </thead>
                <tbody>
        """

        for customer in customers:
            body += '<tr>'
            body += '<td>%s</td>' % customer.id
            body += '<td>%s</td>' % customer.name
            body += '<td>%s</td>' % customer.email
            body += '<td><a href="/9-create-customer-payment?customer_id=%s">Create payment for customer</a></td>' % \
                    customer.id
            body += '<td><a href="/10-customer-payment-history?customer_id=%s">Show payment history</a>' % \
                    customer.id
            body += '</tr>'

        body += "</tbody></table>"

        return body

    except Error as err:
        return 'API call failed: %s' % err


if __name__ == '__main__':
    print(main())
