from ..error import EmbedNotFound


class ObjectBase(dict):
    def __init__(self, data, client):
        """
        Create a new object from API result data.
        """
        super().__init__(data)
        self.client = client

    def _get_property(self, name):
        """Return the named property from dictionary values."""
        if name not in self:
            return None
        return self[name]

    def _get_link(self, name):
        """Return a link by its name."""
        try:
            return self["_links"][name]["href"]
        except (KeyError, TypeError):
            return None

    def get_embedded(self, name: str):
        """
        Get embedded data by its name.

        :param name: The name of the embedded data.
        :type name: str

        :raises EmbedNotFound: When no embedded data with the given name exists.
        """
        try:
            return self["_embedded"][name]
        except KeyError:
            raise EmbedNotFound(name)

    @classmethod
    def get_object_name(cls):
        name = cls.__name__.lower()
        return f"{name}s"

    @classmethod
    def get_resource_class(cls, client):
        raise NotImplementedError  # pragma: no cover
