from typing import TYPE_CHECKING, Any, Dict, List, Tuple, Type

from .base import ObjectBase

if TYPE_CHECKING:
    from ..resources.base import ResourceBase


class UnknownObject(ObjectBase):
    """Mock object for empty lists."""

    @classmethod
    def get_object_name(cls):
        return "unknown"


class ObjectList(ObjectBase):
    current = None

    def __init__(self, result, object_type, client=None):
        # If an empty dataset was injected, we mock the structure that the remainder of the clas expects.
        # TODO: it would be better if the ObjectList was initiated with a list of results, rather than with
        # the full datastructure as it is now, so we can remove all this mucking around with fake data,
        # mocked result objects, and loads of lengthy accessor workarounds everywhere in the ObjectList.
        if result == {}:
            result = {"_embedded": {"unknown": []}, "count": 0}
            object_type = UnknownObject

        super().__init__(result, client)
        self.object_type = object_type

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
            return ObjectList(sliced_result, self.object_type, self.client)

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

    def get_next(self):
        """Return the next set of objects in an ObjectList."""
        url = self._get_link("next")
        resource = self.object_type.get_resource_class(self.client)
        resp = resource.perform_api_call(resource.REST_READ, url)
        return ObjectList(resp, self.object_type, self.client)

    def get_previous(self):
        """Return the previous set of objects in an ObjectList."""
        url = self._get_link("previous")
        resource = self.object_type.get_resource_class(self.client)
        resp = resource.perform_api_call(resource.REST_READ, url)
        return ObjectList(resp, self.object_type, self.client)


class ResultListIterator:
    """
    An iterator for result lists from the API.

    You can iterate through the results. If the initial result indocates pagination,
    a new result page is automatically fetched from the API when the current result page
    is exhausted.

    Note: This iterator should preferably replace the ObjectList as the default
    return value for the ResourceBase.list() method in the future.
    """

    _last: int
    resource: "ResourceBase"
    result_class: Type[ObjectBase]
    next_uri: str
    list_data: List[Dict[str, Any]]

    def __init__(self, resource: "ResourceBase", data: Dict[str, Any]) -> None:
        self.resource = resource
        self.list_data, self.next_uri = self._parse_data(data)
        self._last = -1

    def __iter__(self):
        """Return the iterator."""
        return self

    def __next__(self) -> ObjectBase:
        """
        Return the next result.

        If the list data is exhausted, but a link to further paginated results
        is available, we fetch those results and return the first result of that.
        """
        current = self._last + 1
        try:
            object_data = self.list_data[current]

        except IndexError:
            if self.next_uri:
                # Fetch new results and return the first entry
                self._reinit_from_uri(self.next_uri)
                return next(self)

            else:
                # No more results to return, nor to fetch: this iterator is really exhausted
                raise StopIteration

        else:
            # Return the next result
            self._last = current
            return self.resource.get_resource_object(object_data)

    def _parse_data(self, data: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], str]:
        """
        Extract useful data from the payload.

        We are interested in the following parts:
        - the actual list data, unwrapped
        - links to next results, when results are paginated
        """
        try:
            next_uri = data["_links"]["next"]["href"]
        except TypeError:
            next_uri = ""

        if not hasattr(self, "result_class"):
            # A bit klunky: need to instantiate the class with fake data, only to get its type.
            #
            # This could be improved if we define the result class (or its dotted path) as a
            # class constant on the resource. Additionaly, that could help when making
            # get_resource_object() a generic method on ResourceBase.
            self.result_class = type(self.resource.get_resource_object({}))

        resource_name = self.result_class.get_object_name()
        list_data = data["_embedded"][resource_name]

        return list_data, next_uri

    def _reinit_from_uri(self, uri: str) -> None:
        """Fetch additional results from the API, and feed the iterator with the data."""

        result = self.resource.perform_api_call(self.resource.REST_READ, uri)
        self.list_data, self.next_uri = self._parse_data(result)
        self._last = -1
