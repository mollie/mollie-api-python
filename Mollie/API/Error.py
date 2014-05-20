class Error(Exception):
    def __init__(self, message=None, field=None):
        self.message = message
        self.field = field