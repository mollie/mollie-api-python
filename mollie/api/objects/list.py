from .base import Base


class List(Base):
    def __init__(self, result, object_type):
        Base.__init__(self, result)
        self.object_type = object_type

    def getResourceName(self):
        return self.object_type.__name__.lower() + 's'

    def __iter__(self):
        for item in self['_embedded'][self.getResourceName()]:
            yield self.object_type(item)

    @property
    def count(self):
        if 'count' not in self:
            return None
        return int(self['count'])

    def getOffset(self):
        if 'offset' not in self:
            return None
        return self['offset']
