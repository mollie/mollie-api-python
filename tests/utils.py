from mollie.api.objects.list import List


def assert_list_object(list, object_type):
    """Assert that a List object is correctly working, and has sane contents."""
    assert isinstance(list, List), 'Object {obj} is not a List instance.'.format(obj=list)
    assert isinstance(list.count, int), 'List count is not an integer.'
    assert list.count > 0

    # verify items in list
    items = []
    for item in list:
        assert isinstance(item, object_type)
        assert item.id is not None
        items.append(item.id)

    assert len(items) == list.count, "Items in list don't match list count."
    assert len(set(items)) == list.count, 'Not all object ids in the list are unique.'
