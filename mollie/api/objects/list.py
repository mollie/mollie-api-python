from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Optional, Type

from .base import ObjectBase

if TYPE_CHECKING:
    from mollie.api.client import Client
    from mollie.api.resources.base import ResourceBase


class ListBase(ObjectBase, ABC):
    current = None

    def __len__(self):
        """Return the count field."""
        return self.count

    def __iter__(self):
        """Implement iterator interface."""
        self.current = None
        return self

    def __next__(self):
        """Implement iterator interface."""
        if self.current is None:
            self.current = 0
        else:
            self.current += 1
        try:
            item = self["_embedded"][self.object_type.get_object_name()][self.current]
            return self.object_type(item, self.client)
        except IndexError:
            self.current = None
            raise StopIteration

    def __getitem__(self, key):
        """Implement Sequence interface."""
        object_name = self.object_type.get_object_name()
        if isinstance(key, int):
            # Return an index-based search from the "_embedded" dataset
            item = self["_embedded"][object_name][key]
            return self.object_type(item, self.client)

        if isinstance(key, slice):
            _start = key.start or 0
            _stop = key.stop or self["count"]
            _step = key.step or 1
            sliced_data = [self["_embedded"][object_name][x] for x in range(_start, _stop, _step)]
            # Now we mock a result based on the sliced data
            sliced_result = {
                "_embedded": {
                    object_name: sliced_data,
                },
                "count": len(sliced_data),
            }
            return self.new(sliced_result)

        return super().__getitem__(key)

    @property
    def count(self):
        if "count" not in self:
            return None
        return int(self["count"])

    def has_next(self):
        """Return True if the ObjectList contains an url for the next set."""
        return self._get_link("next") is not None

    def has_previous(self):
        """Return True if the ObjectList contains an url for the previous set."""
        return self._get_link("previous") is not None

    @abstractmethod
    def get_next(self): ...

    @abstractmethod
    def get_previous(self): ...

    @property
    @abstractmethod
    def object_type(self): ...

    @abstractmethod
    def new(self, result): ...


class PaginationList(ListBase):
    """
    Pagination lists are used to return a paginated list of Objects.

    You can use the `has_next` and `get_next` methods to get the next page of result data from the API.
    The `has_previous` and `get_previous` methods return the previous page.
    """

    _parent: "ResourceBase"

    def __init__(self, result: Any, parent: "ResourceBase", client: "Client"):
        # If an empty dataset was injected, we mock the structure that the remainder of the clas expects.
        # TODO: it would be better if the ObjectList was initiated with a list of results, rather than with
        # the full datastructure as it is now, so we can remove all this mucking around with fake data,
        # mocked result objects, and loads of lengthy accessor workarounds everywhere in the ObjectList.
        self._parent = parent

        if result == {}:
            result = {"_embedded": {f"{self._parent.object_type.get_object_name()}": []}, "count": 0}

        super().__init__(result, client)

    def get_next(self):
        """Return the next set of objects in the paginated list."""
        url = self._get_link("next")
        if url is None:
            return None
        resp = self._parent.perform_api_call(self._parent.REST_READ, url)
        return PaginationList(resp, self._parent, self.client)

    def get_previous(self):
        """Return the previous set of objects in the paginated list."""
        url = self._get_link("previous")
        if url is None:
            return None
        resp = self._parent.perform_api_call(self._parent.REST_READ, url)
        return PaginationList(resp, self._parent, self.client)

    @property
    def object_type(self):
        return self._parent.object_type

    def new(self, result):
        return PaginationList(result, self._parent, self.client)


class ObjectList(ListBase):
    """
    Object lists are used to return an embedded list on an object.

    It works to similar to PaginationList, but has no pagination (as all data is already embedded).
    """

    _object_type: Type[ObjectBase]

    def __init__(self, result: Any, object_type: Type[ObjectBase], client: Optional["Client"] = None):
        # If an empty dataset was injected, we mock the structure that the remainder of the clas expects.
        # TODO: it would be better if the ObjectList was initiated with a list of results, rather than with
        # the full datastructure as it is now, so we can remove all this mucking around with fake data,
        # mocked result objects, and loads of lengthy accessor workarounds everywhere in the ObjectList.
        self._object_type = object_type

        if result == {}:
            result = {"_embedded": {f"{self._object_type.get_object_name()}": []}, "count": 0}

        super().__init__(result, client)

    def get_next(self):
        """Return the next set of objects in an ObjectList."""
        return None

    def get_previous(self):
        return None

    @property
    def object_type(self):
        return self._object_type

    def new(self, result):
        return ObjectList(result, self._object_type, self.client)
