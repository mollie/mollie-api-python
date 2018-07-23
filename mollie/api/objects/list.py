from .base import Base


class List(Base):
    def __init__(self, result, object_type):
        Base.__init__(self, result)
        self.object_type = object_type

    def get_object_name(self):
        return self.object_type.__name__.lower() + 's'

    def __iter__(self):
        for item in self['_embedded'][self.get_object_name()]:
            yield self.object_type(item)

    @property
    def count(self):
        if 'count' not in self:
            return None
        return int(self['count'])

    def get_offset(self):
        if 'offset' not in self:
            return None
        return self['offset']
