class Base(dict):

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
