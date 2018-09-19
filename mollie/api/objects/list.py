from .base import Base


class List(Base):
    current = None
    client = None

    def __init__(self, result, object_type, client=None):
        Base.__init__(self, result)
        self.object_type = object_type
        self.client = client

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
