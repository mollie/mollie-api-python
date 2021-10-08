from .base import ObjectBase


class Issuer(ObjectBase):
    @property
    def resource(self):
        return self._get_property("resource")

    @property
    def id(self):
        return self._get_property("id")

    @property
    def name(self):
        return self._get_property("name")

    @property
    def image_svg(self):
        images = self._get_property("image")
        return images["svg"]

    @property
    def image_size1x(self):
        images = self._get_property("image")
        return images["size1x"]

    @property
    def image_size2x(self):
        images = self._get_property("image")
        return images["size2x"]
