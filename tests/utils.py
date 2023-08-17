from mollie.api.objects.list import ListBase


def assert_list_object(obj, object_type, count=None):
    """Assert that a List object is correctly working, and has sane contents."""
    assert isinstance(obj, ListBase), f"Object {obj} is not a ListBase instance."
    assert isinstance(obj.count, int), "ObjectList count is not an integer."
    if count is not None:
        assert obj.count == count, "ObjectList does not contain the expected number of items."
    else:
        assert obj.count > 0, "ObjectList has no items."

    # verify items in list
    items = []
    for item in obj:
        assert isinstance(item, object_type)
        assert item.id is not None
        items.append(item.id)

    assert len(items) == obj.count, "Items in ObjectList don't match list count."
    assert len(set(items)) == obj.count, "Not all object ids in the ObjectList are unique."


def assert_empty_object(obj, object_type):
    """Assert that an object is empty and of the given type."""
    assert isinstance(obj, object_type)
    assert obj == {}, "Dict representaton of the object should be empty."
    assert obj.resource is None, "A resource property should not be available."
    assert obj.id is None, "An id resource property should not be available."
