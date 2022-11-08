from .base import ObjectBase


class Client(ObjectBase):
    @classmethod
    def get_resource_class(cls, client):
        from ..resources import Clients

        return Clients(client)

    # Documented properties

    @property
    def id(self):
        return self._get_property("id")

    @property
    def resource(self):
        return self._get_property("resource")

    @property
    def organisation_created_at(self):
        return self._get_property("organizationCreatedAt")

    # documented _links

    def get_organization(self):
        """Return the client’s organization. Only available when the include could have been used."""
        url = self._get_link("organization")
        if url:
            return self.client.organizations.from_url(url)
        else:
            return None

    def get_onboarding(self):
        """Return the client’s onboarding status. Only available when the include could have been used."""
        url = self._get_link("onboarding")
        if url:
            return self.client.onboarding.from_url(url)
        else:
            return None
