import pytest

from mollie.api.objects.list import PaginationList
from mollie.api.objects.method import Method

from .utils import assert_list_object


def test_list_iterator_behaviour(client, response):
    """Verify the behaviour of the List object in iterator circumstances."""
    response.get("https://api.mollie.com/v2/methods", "methods_list")

    methods = client.methods.list()
    assert isinstance(methods, PaginationList)

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
    assert iterated == len(methods)

    # use for loop as iterator
    iterated = 0
    for item in methods:
        assert isinstance(item, Method)
        iterated += 1

    assert iterated == methods.count


def test_list_multiple_iterations(client, response):
    """Verify that we can iterate a list multiple times."""
    response.get("https://api.mollie.com/v2/methods", "methods_list")

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
    response.get("https://api.mollie.com/v2/customers?limit=5", "customers_list_first")
    response.get("https://api.mollie.com/v2/customers?from=cst_8pknKQJzJa&limit=5", "customers_list_second")
    response.get("https://api.mollie.com/v2/customers?from=cst_prs8JjDf57&limit=5", "customers_list_third")
    response.get("https://api.mollie.com/v2/customers?from=cst_g328m9rhGe&limit=5", "customers_list_fourth")
    response.get("https://api.mollie.com/v2/customers?from=cst_prs8JjDf57&limit=5", "customers_list_third")
    response.get("https://api.mollie.com/v2/customers?from=cst_8pknKQJzJa&limit=5", "customers_list_second")
    response.get("https://api.mollie.com/v2/customers?from=cst_HwBHgJgRAf&limit=5", "customers_list_first")

    customers = client.customers.list(limit=5)
    assert customers.count == 5
    forward_first_id = next(customers).id
    customer_ids = [customer.id for customer in customers]
    while customers.has_next():
        customers = customers.get_next()
        for customer in customers:
            customer_ids.append(customer.id)

    assert len(customer_ids) == 17, "Unexpected number of customers"
    assert len(set(customer_ids)) == 17, "Unexpected number of unique customers"

    # now reverse the behaviour
    while customers.has_previous():
        customers = customers.get_previous()
    reverse_last_id = next(customers).id

    assert (
        forward_first_id == reverse_last_id
    ), "Expected the first customer of the first page to be stable, but it wasn't"


def test_list_supports_integer_sequences(client, response):
    response.get("https://api.mollie.com/v2/customers", "customers_list")

    customers = client.customers.list()
    first_customer = customers[1]
    assert first_customer.id == "cst_8wmqcHMN4y", "Getting a customer by index should be possible"

    last_customer = customers[-1]
    assert last_customer.id == "cst_8wmqcHMN4x", "Getting a customer by negative index should be possible"

    with pytest.raises(IndexError) as excinfo:
        customers[1000]
    assert str(excinfo.value) == "list index out of range", "A non-existent index should raise an IndexError"


def test_list_supports_slice_sequences(client, response):
    response.get("https://api.mollie.com/v2/methods", "methods_list")

    methods = client.methods.list()
    # Baseline for result checks
    assert [x.id for x in methods] == [
        "ideal",
        "creditcard",
        "paypal",
        "bancontact",
        "banktransfer",
        "sofort",
        "kbc",
        "belfius",
        "inghomepay",
        "giftcard",
    ]

    sliced = methods[1:3]
    assert_list_object(sliced, Method, 2), "Slicing should be possible"
    assert [x.id for x in sliced] == ["creditcard", "paypal"]

    slice_forward = methods[5:]
    assert_list_object(slice_forward, Method, 5), "Slicing forward should possible"
    assert [x.id for x in slice_forward] == ["sofort", "kbc", "belfius", "inghomepay", "giftcard"]

    slice_backwards = methods[:3]
    assert_list_object(slice_backwards, Method, 3), "Slicing backwards should be possible"
    assert [x.id for x in slice_backwards] == ["ideal", "creditcard", "paypal"]

    slice_stepped = methods[0:5:2]
    assert_list_object(slice_stepped, Method, 3), "Slicing with a step value should be possble"
    assert [x.id for x in slice_stepped] == ["ideal", "paypal", "banktransfer"]

    slice_step_only = methods[::3]
    assert_list_object(slice_step_only, Method, 4), "Slicing with only a step value should be possible"
    assert [x.id for x in slice_step_only] == ["ideal", "bancontact", "kbc", "giftcard"]
