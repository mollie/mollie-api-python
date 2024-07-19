import warnings

from .base import ObjectBase
from ..error import ClosedBetaWarning


class ClientLink(ObjectBase):

    def __init__(self, data, client):
        warnings.warn(
            "The Client Links API is in closed beta and only available to "
            "selected partners. Please contact your partner manager if you "
            "want to implement this.",
            ClosedBetaWarning,
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
