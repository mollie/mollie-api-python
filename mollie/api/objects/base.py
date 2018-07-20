class Base(dict):

    def _get_property(self, name):
        """Return the named property from dictionary values."""
        if not self[name]:
            return None
        return self[name]
