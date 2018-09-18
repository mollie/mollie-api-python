class Base(dict):

    _resource = None

    def __init__(self, data, resource=None):
        """
        Create a new object from API result data.

        We optionally initialize the _resource variable to be able to use this when querying the API
        for additional data defined as an endpoint in the _links attribute.
        """
        super(Base, self).__init__(data)
        self._resource = resource

    def _get_property(self, name):
        """Return the named property from dictionary values."""
        if name not in self:
            return None
        return self[name]

    def _get_link(self, name):
        """Return a link by its name."""
        try:
            return self['_links'][name]['href']
        except KeyError:
            return None

    @classmethod
    def get_object_name(cls):
        return '{name}s'.format(name=cls.__name__.lower())
