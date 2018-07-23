from mollie.api.objects.list import List
from mollie.api.objects.method import Method


def test_list_iterator_behaviour(client, response):
    """Verify the behaviour of the List object in iterator curcumstances."""
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
