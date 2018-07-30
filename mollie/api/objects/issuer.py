from .base import Base


class Issuer(Base):
    @property
    def resource(self):
        try:
            return self._get_property('resource')
        except KeyError:
            return None

    @property
    def id(self):
        try:
            return self._get_property('id')
        except KeyError:
            return None

    @property
    def name(self):
        try:
            return self._get_property('name')
        except KeyError:
            return None

    @property
    def image_size1x(self):
        try:
            images = self._get_property('image')
            return images['size1x']
        except KeyError:
            return None

    @property
    def image_size2x(self):
        try:
            images = self._get_property('image')
            return images['size2x']
        except KeyError:
            return None
