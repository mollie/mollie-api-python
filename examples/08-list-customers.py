# coding=utf-8
#
# Example: Retrieving all of your customers with offset and count
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
        customers = mollie_client.customers.list(**params)

        body = ''

        if not len(customers):
            body += '<p>You have no customers. You can create one from the examples.</p>'
            return body

        body += '<p>Showing the last {num} customers for your API key.</p>'.format(num=len(customers))

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
            body += '<td>{id}</td>'.format(id=customer.id)
            body += '<td>{name}</td>'.format(name=customer.name)
            body += '<td>{email}</td>'.format(email=customer.email)
            body += '<td><a href="/09-create-customer-payment?customer_id={id}">' \
                'Create payment for customer</a></td>'.format(id=customer.id)
            body += '<td><a href="/10-customer-payment-history?customer_id={id}">Show payment history</a>'.format(
                id=customer.id)
            body += '</tr>'

        body += "</tbody></table>"

        return body

    except Error as err:
        return 'API call failed: {error}'.format(error=err)


if __name__ == '__main__':
    print(main())
