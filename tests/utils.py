from mollie.api.objects.list import Collection


def assert_list_object(obj, object_type, count=None):
    """Assert that a List object is correctly working, and has sane contents."""
    assert isinstance(obj, Collection), f"Object {obj} is not a Collection instance."
    assert isinstance(obj.count, int), "Collection count is not an integer."
    if count is not None:
        assert obj.count == count, "Collection does not contain the expected number of items."
    else:
        assert obj.count > 0, "Collection has no items."

    # verify items in list
    items = []
    for item in obj:
        assert isinstance(item, object_type)
        assert item.id is not None
        items.append(item.id)

    assert len(items) == obj.count, "Items in Collection don't match list count."
    assert len(set(items)) == obj.count, "Not all object ids in the Collection are unique."
