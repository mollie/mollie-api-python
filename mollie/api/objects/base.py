class Base(dict):

    def _get_property(self, name):
        """Return the named property from dictionary values."""
        if name not in self:
            return None
        return self[name]
