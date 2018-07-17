class Base(dict):

    def getProperty(self, name):
        """Return the named property from dictionary values."""
        if not self[name]:
            return None
        return self[name]
