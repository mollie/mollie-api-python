class Error(Exception):
    def __init__(self, message=None, field=None):
        Exception.__init__(self, message)
        self.field = field
