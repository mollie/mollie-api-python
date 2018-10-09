from .base import Base


class List(Base):
    current = None

    def __init__(self, result, object_type, client=None):
        super(List, self).__init__(result, client=client)
        self.object_type = object_type

    def __len__(self):
        """Return the count field."""
        return int(self['count'])

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
            item = self['_embedded'][self.object_type.get_object_name()][self.current]
            return self.object_type(item, client=self.client)
        except IndexError:
            self.current = None
            raise StopIteration

    next = __next__  # support python2 iterator interface

    @property
    def count(self):
        if 'count' not in self:
            return None
        return int(self['count'])

    def has_next(self):
        """Return True if the list contains an url for the next set"""
        return self._get_link('next') is not None

    def has_previous(self):
        """Return True if the list contains an url for the previous set"""
        return self._get_link('previous') is not None

    def get_next(self):
        """Return the next set of objects in a list"""
        url = self._get_link('next')
        resource = self.object_type.get_resource_class(self.client)
        resp = resource.perform_api_call(resource.REST_READ, url)
        return List(resp, self.object_type, client=self.client)

    def get_previous(self):
        """Return the previous set of objects in a list"""
        url = self._get_link('previous')
        resource = self.object_type.get_resource_class(self.client)
        resp = resource.perform_api_call(resource.REST_READ, url)
        return List(resp, self.object_type, client=self.client)
