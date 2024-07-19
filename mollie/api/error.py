class Error(Exception):
    """Base exception."""

    pass


class RequestError(Error):
    """Errors while preparing or performing an API request."""

    pass


class RequestSetupError(RequestError):
    """Errors while preparing an API request."""

    pass


class IdentifierError(RequestSetupError):
    """Errors related to invalid resource identifiers that will be requested from the API."""

    pass


class ResponseHandlingError(Error):
    """Errors related to handling the response from the API.

    When receiving an error while performing a POST, PATCH or DELETE action,
    an idempotency_key is available that can be used for replicating the request.
    """

    idempotency_key = ""

    def __init__(self, message, idempotency_key=""):
        super().__init__(message)
        self.idempotency_key = idempotency_key


class ResponseError(Error):
    """Errors reported by the API.

    When receiving an error while performing a POST, PATCH or DELETE action,
    an idempotency_key is available that can be used for replicating the request.
    """

    status = None
    field = None
    idempotency_key = ""

    def __init__(self, resp=None, idempotency_key=""):
        message = resp["detail"]
        super().__init__(message)
        self.status = resp["status"]
        if "field" in resp:
            self.field = resp["field"]

        self.idempotency_key = idempotency_key

    @staticmethod
    def factory(resp, idempotency_key=""):
        """Return a ResponseError subclass based on the API payload.

        All errors are documented: https://docs.mollie.com/guides/handling-errors#all-possible-status-codes
        More exceptions should be added here when appropriate, and when useful examples of API errors are available.
        """
        status = resp["status"]
        if status == 400:
            return BadRequestError(resp, idempotency_key=idempotency_key)
        elif status == 401:
            return UnauthorizedError(resp, idempotency_key=idempotency_key)
        elif status == 404:
            return NotFoundError(resp, idempotency_key=idempotency_key)
        elif status == 409:
            return ConflictError(resp, idempotency_key=idempotency_key)
        elif status == 422:
            return UnprocessableEntityError(resp, idempotency_key=idempotency_key)
        else:
            # generic fallback
            return ResponseError(resp, idempotency_key=idempotency_key)

    def __reduce__(self):
        """
        Customize the pickling routine.

        Exceptions have a custom __reduce__() routine, but that doesn't work
        since we override the __init__ method here.
        """

        callable_ = self.__class__
        args = (
            {
                "detail": self.args[0],
                "status": self.status,
                "field": self.field,
            },
            self.idempotency_key,
        )
        return (callable_, args)


class UnauthorizedError(ResponseError):
    """Your request wasn't executed due to failed authentication. Check your API key."""

    pass


class NotFoundError(ResponseError):
    """The object referenced by your API request does not exist."""

    pass


class BadRequestError(ResponseError):
    pass


class ConflictError(ResponseError):
    pass


class UnprocessableEntityError(ResponseError):
    """We could not process your request due to another reason than the ones listed above.

    The response usually contains a field property to indicate which field is causing the issue.
    """

    pass


class DataConsistencyError(Error):
    """We could not process the API response due to an inconsistency.

    We received different data than expected from the API.
    """

    pass


class EmbedNotFound(Error):
    """We could not access requested data with an object because the required embed was missing.

    Some data within an object is only available after it is explicitly requested using an embed query parameter.
    You tried to access data which is available from an embed, but the data is missing: apparently you forgot
    to set the related embed parameter.
    """

    def __init__(self, name):
        msg = f"You tried to access embedded data, but did not request to embed '{name}' in the request."
        super().__init__(msg)


"""
Deprecation policy

When a minor version release will be done, remove all code that triggers the DeprecationWarning subclass.
Then rename the DeprecationWarning subclass to the next minor version (RemovedIn24Warning => RemovedIn25Warning).
and rename the PendingDeprecation subclass below also.

This will make all existing PendingDeprecationWarnings change to DeprecationWarnings.

This deprecation policy is similar to what is used in Django and Django-rest-framework.
See https://www.django-rest-framework.org/community/release-notes/#deprecation-policy for details.
"""


class RemovedIn27Warning(DeprecationWarning):
    """Deprecation warning for features that will be removed in version 2.7.0."""

    pass


class RemovedIn28Warning(PendingDeprecationWarning):
    """Pending deprecation warning for features that will be removed in version 2.8.0."""

    pass


class APIDeprecationWarning(DeprecationWarning):
    """
    Features that are deprecated in the Mollie API.

    This library cannot control when an API feature will be removed. We can only label it as 'deprecated'
    using this warning, and hope that library users stop using the feature before the removal.
    """

    pass


"""
Beta policy

Beta API may be subject to changes and is not covered by our versioning policy.
"""


class OpenBetaWarning(UserWarning):
    """Warning for features that in open beta."""

    pass
