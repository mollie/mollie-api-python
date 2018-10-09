from mollie.api.objects.list import List
from mollie.api.objects.method import Method


def test_list_iterator_behaviour(client, response):
    """Verify the behaviour of the List object in iterator circumstances."""
    response.get('https://api.mollie.com/v2/methods', 'methods_list')

    methods = client.methods.list()
    assert isinstance(methods, List)

    # walk the list using next()
    iterated = 0
    while True:
        try:
            item = next(methods)
            assert isinstance(item, Method)
            iterated += 1
        except StopIteration:
            # read all items from the iterator
            break

    assert iterated == methods.count

    # use for loop as iterator
    iterated = 0
    for item in methods:
        assert isinstance(item, Method)
        iterated += 1

    assert iterated == methods.count


def test_list_multiple_iterations(client, response):
    """Verify that we can iterate a list multiple times."""
    response.get('https://api.mollie.com/v2/methods', 'methods_list')

    methods = client.methods.list()
    # iterate once using next()
    items_first_run = 0
    while True:
        try:
            next(methods)
            items_first_run += 1
        except StopIteration:
            break
    assert items_first_run == methods.count

    # iterate again
    items_second_run = 0
    while True:
        try:
            next(methods)
            items_second_run += 1
        except StopIteration:
            break
    assert items_second_run == methods.count

    methods = client.methods.list()
    # iterate once using for loop
    items_third_run = 0
    for item in methods:
        items_third_run += 1
    assert items_third_run == methods.count
    # iterate again
    items_fourth_run = 0
    for item in methods:
        items_fourth_run += 1
    assert items_fourth_run == methods.count


def test_list_multiple_api_calls(client, response):
    """Verify that we can iterate over a paginated result set."""
    response.get('https://api.mollie.com/v2/customers?limit=5', 'customers_list_first')
    response.get('https://api.mollie.com/v2/customers?from=cst_8pknKQJzJa&limit=5', 'customers_list_second')
    response.get('https://api.mollie.com/v2/customers?from=cst_prs8JjDf57&limit=5', 'customers_list_third')
    response.get('https://api.mollie.com/v2/customers?from=cst_g328m9rhGe&limit=5', 'customers_list_fourth')
    response.get('https://api.mollie.com/v2/customers?from=cst_prs8JjDf57&limit=5', 'customers_list_third')
    response.get('https://api.mollie.com/v2/customers?from=cst_8pknKQJzJa&limit=5', 'customers_list_second')
    response.get('https://api.mollie.com/v2/customers?from=cst_HwBHgJgRAf&limit=5', 'customers_list_first')

    customers = client.customers.list(limit=5)
    assert customers.count == 5
    forward_first_id = next(customers).id
    customer_ids = [customer.id for customer in customers]
    while customers.has_next():
        customers = customers.get_next()
        for customer in customers:
            customer_ids.append(customer.id)

    assert len(customer_ids) == 17, 'Unexpected number of customers'
    assert len(set(customer_ids)) == 17, 'Unexpected number of unique customers'

    # now reverse the behaviour
    while customers.has_previous():
        customers = customers.get_previous()
    reverse_last_id = next(customers).id

    assert forward_first_id == reverse_last_id, \
        "Expected the first customer of the first page to be stable, but it wasn't"
