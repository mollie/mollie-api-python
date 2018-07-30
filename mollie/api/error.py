class Error(Exception):
    """Base exception."""

    def __init__(self, message=None, field=None):
        Exception.__init__(self, message)
        self.field = field


class RequestError(Error):
    """Errors while preparing or performing an API request."""

    pass


class RequestSetupError(RequestError):
    """Errors while preparing an API request."""

    pass


class IdentifierValidationError(RequestSetupError):
    """Errors related to invalid identifiers for objects that will be requested from the API."""

    pass


class ResponseHandlingError(Error):
    """Errors related to handling the response from the API."""

    pass


class ResponseError(Error):
    """Errors reported by the API."""

    status = None

    def __init__(self, resp=None, field=None):
        import ipdb; ipdb.set_trace()  # noqa
        message = resp['detail']
        super(ResponseError, self).__init__(message, field)
        self.status = resp['status_code']
