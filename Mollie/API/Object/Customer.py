from .Base import Base


class Customer(Base):
    @property
    def id(self):
        if 'id' not in self:
            return None
        return self.getProperty('id')

    @property
    def name(self):
        if 'name' not in self:
            return None
        return self.getProperty('name')

    @property
    def email(self):
        if 'email' not in self:
            return None
        return self.getProperty('email')

    @property
    def locale(self):
        if 'locale' not in self:
            return None
        return self.getProperty('locale')

    @property
    def metadata(self):
        if 'metadata' not in self:
            return None
        return self.getProperty('metadata')

    @property
    def mode(self):
        if 'mode' not in self:
            return None
        return self.getProperty('mode')

    @property
    def resource(self):
        if 'resource' not in self:
            return None
        return self.getProperty('resource')

    @property
    def createdAt(self):
        if 'createdAt' not in self:
            return None
        return self.getProperty('createdAt')

