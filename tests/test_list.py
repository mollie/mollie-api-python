import pytest

from mollie.api.objects.list import List
from mollie.api.objects.method import Method


def test_list_iterator_behaviour(client, response):
    """Verify the behaviour of the List object in iterator circumstances."""
    response.get('https://api.mollie.com/v2/methods', 'methods_multiple')

    methods = client.methods.all()
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


@pytest.mark.xfail(strict=True, reason="Pagination interface is still undecided")
def test_list_multiple_api_calls(client, response):
    """
    Verify that we can iterate over a paginated result set.

    The interface using get_next()/get_previous() is not optimal due to the fact that we cant't
    retrieve the complete dataset count from the api. When that would be possible, we could implement
    the List object to handle the next and previous links transparently when iterating over results.
    """
    response.get('https://api.mollie.com/v2/customers?limit=5', 'customers_list_first')
    response.get('https://api.mollie.com/v2/customers?from=cst_8pknKQJzJa&limit=5', 'customers_list_second')
    response.get('https://api.mollie.com/v2/customers?from=cst_prs8JjDf57&limit=5', 'customers_list_third')
    response.get('https://api.mollie.com/v2/customers?from=cst_g328m9rhGe&limit=5', 'customers_list_fourth')
    response.get('https://api.mollie.com/v2/customers?from=cst_prs8JjDf57&limit=5', 'customers_list_third')
    response.get('https://api.mollie.com/v2/customers?from=cst_8pknKQJzJa&limit=5', 'customers_list_second')
    response.get('https://api.mollie.com/v2/customers?from=cst_HwBHgJgRAf&limit=5', 'customers_list_first')

    customers = client.customers.all(limit=5)
    assert customers.count == 5
    all_customers_count = customers.count
    while customers.has_next():
        customers = customers.get_next()
        all_customers_count += customers.count

    assert all_customers_count == 17

    # now reverse the behaviour
    while customers.has_previous():
        customers = customers.get_previous()
        all_customers_count -= customers.count

    assert all_customers_count == 5
