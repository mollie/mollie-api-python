class Error(Exception):
    """Base exception."""

    def __init__(self, message):
        Exception.__init__(self, message)


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
    field = None

    def __init__(self, resp=None):
        message = resp['detail']
        super(ResponseError, self).__init__(message)
        self.status = resp['status']
        if 'field' in resp:
            self.field = resp['field']

    @staticmethod
    def factory(resp):
        """
        Return a ResponseError subclass based on the API payload.

        All error are documented: https://docs.mollie.com/guides/handling-errors#all-possible-status-codes
        More exceptions should be added here when appropriate, and when useful examples of API errors are available.
        """
        status = resp['status']
        if status == 401:
            return UnauthorizedError(resp)
        elif status == 404:
            return NotFoundError(resp)
        elif status == 422:
            return UnprocessableEntityError(resp)
        else:
            # generic fallback
            return ResponseError(resp)


class UnauthorizedError(ResponseError):
    """Your request wasn't executed due to failed authentication. Check your API key."""

    pass


class NotFoundError(ResponseError):
    """The object referenced by your API request does not exist."""

    pass


class UnprocessableEntityError(ResponseError):
    """
    We could not process your request due to another reason than the ones listed above.

    The response usually contains a field property to indicate which field is causing the issue.
    """

    pass
