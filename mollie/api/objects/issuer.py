from .base import Base


class Issuer(Base):

    @property
    def resource(self):
        return self._get_property('resource')

    @property
    def id(self):
        return self._get_property('id')

    @property
    def name(self):
        return self._get_property('name')

    @property
    def image_svg(self):
        try:
            images = self._get_property('image')
            return images['svg']
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
