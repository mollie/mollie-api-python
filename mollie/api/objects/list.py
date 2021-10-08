from .base import ObjectBase


class Collection(ObjectBase):
    current = None

    def __init__(self, result, object_type, client=None):
        super().__init__(result, client)
        self.object_type = object_type

    def __len__(self):
        """Return the count field."""
        return int(self["count"])

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
            return Collection(sliced_result, self.object_type, self.client)

        return super().__getitem__(key)

    @property
    def count(self):
        if "count" not in self:
            return None
        return int(self["count"])

    def has_next(self):
        """Return True if the list contains an url for the next set"""
        return self._get_link("next") is not None

    def has_previous(self):
        """Return True if the list contains an url for the previous set"""
        return self._get_link("previous") is not None

    def get_next(self):
        """Return the next set of objects in a list"""
        url = self._get_link("next")
        resource = self.object_type.get_resource_class(self.client)
        resp = resource.perform_api_call(resource.REST_READ, url)
        return Collection(resp, self.object_type, self.client)

    def get_previous(self):
        """Return the previous set of objects in a list"""
        url = self._get_link("previous")
        resource = self.object_type.get_resource_class(self.client)
        resp = resource.perform_api_call(resource.REST_READ, url)
        return Collection(resp, self.object_type, self.client)
