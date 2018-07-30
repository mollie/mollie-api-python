class Error(Exception):
    """Base exception."""

    def __init__(self, message=None, field=None):
        Exception.__init__(self, message)
        self.field = field


class RequestError(Error):
    """Errors while preparing or performing an API request."""

    pass


class RequestSetupError(RequestError):
    """Errors related to setting up the request."""

    pass
