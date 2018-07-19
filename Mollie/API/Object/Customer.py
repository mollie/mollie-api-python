from .Base import Base


class Customer(Base):
    @property
    def id(self):
        return self.getProperty('id')

    @property
    def name(self):
        return self.getProperty('name')

    @property
    def email(self):
        return self.getProperty('email')

    @property
    def locale(self):
        return self.getProperty('locale')

    @property
    def metadata(self):
        return self.getProperty('metadata')

    @property
    def mode(self):
        return self.getProperty('mode')

    @property
    def resource(self):
        return self.getProperty('resource')

    @property
    def createdAt(self):
        return self.getProperty('createdAt')
