from .base import Base


class List(Base):
    current = None

    def __init__(self, result, object_type):
        Base.__init__(self, result)
        self.object_type = object_type

    def __len__(self):
        """Return the count field."""
        return int(self['count'])

    def get_object_name(self):
        return self.object_type.__name__.lower() + 's'

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
            item = self['_embedded'][self.get_object_name()][self.current]
            return self.object_type(item)
        except IndexError:
            raise StopIteration

    next = __next__  # support python2 iterator interface

    @property
    def count(self):
        if 'count' not in self:
            return None
        return int(self['count'])
