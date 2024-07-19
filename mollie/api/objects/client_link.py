import warnings

from ..error import OpenBetaWarning
from .base import ObjectBase


class ClientLink(ObjectBase):

    def __init__(self, data, client):
        warnings.warn(
            "ClientLink is currently in open beta, and the final specification may still change.",
            OpenBetaWarning,
        )
        super().__init__(data, client)

    @classmethod
    def get_object_name(cls):
        return "client_links"

    # Documented properties

    @property
    def resource(self):
        return self._get_property("resource")

    @property
    def id(self):
        return self._get_property("id")

    # documented _links

    @property
    def link(self):
        return self._get_link("self")

    @property
    def client_link(self):
        return self._get_link("clientLink")

    @property
    def documentation_link(self):
        return self._get_link("documentation")
