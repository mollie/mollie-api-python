from .Base import Base


class Customer(Base):
    @property
    def id(self):
        if 'id' not in self:
            return None
        return self['id']

    @property
    def name(self):
        if 'name' not in self:
            return None
        return self['name']

    @property
    def email(self):
        if 'email' not in self:
            return None
        return self['email']

    @property
    def locale(self):
        if 'locale' not in self:
            return None
        return self['locale']

    @property
    def metadata(self):
        if 'metadata' not in self:
            return None
        return self['metadata']

    @property
    def mode(self):
        if 'metadata' not in self:
            return None
        return self['metadata']

    @property
    def resource(self):
        if 'resource' not in self:
            return None
        return self['resource']

    @property
    def createdAt(self):
        if 'createdAt' not in self:
            return None
        return self['createdAt']

