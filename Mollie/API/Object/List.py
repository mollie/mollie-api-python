from .Base import *


class List(Base):
    def __init__(self, result, object_type):
        Base.__init__(self, result)
        self.object_type = object_type

    def __iter__(self):
        for item in self['data']:
            yield self.object_type(item)

    def getTotalCount(self):
        if 'totalCount' not in self:
            return None
        return self['totalCount']

    def getOffset(self):
        if 'offset' not in self:
            return None
        return self['offset']

    def getCount(self):
        if 'count' not in self:
            return None
        return self['count']
