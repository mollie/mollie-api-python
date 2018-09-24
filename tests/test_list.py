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
    all_customers_count = customers.count
    first_customer = next(customers).id
    while customers.has_next():
        customers = customers.get_next()
        all_customers_count += customers.count

    assert all_customers_count == 17

    # now reverse the behaviour
    while customers.has_previous():
        customers = customers.get_previous()
        all_customers_count -= customers.count

    assert next(customers).id == first_customer
