from mollie.api.objects.list import List


def assert_list_object(obj, object_type):
    """Assert that a List object is correctly working, and has sane contents."""
    assert isinstance(obj, List), 'Object {obj} is not a List instance.'.format(obj=obj)
    assert isinstance(obj.count, int), 'List count is not an integer.'
    assert obj.count > 0

    # verify items in list
    items = []
    for item in obj:
        assert isinstance(item, object_type)
        assert item.id is not None
        items.append(item.id)

    assert len(items) == obj.count, "Items in list don't match list count."
    assert len(set(items)) == obj.count, 'Not all object ids in the list are unique.'
