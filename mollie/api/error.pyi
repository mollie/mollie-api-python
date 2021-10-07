from typing import Any


class Error(Exception):
    ...


class RequestError(Error):
    ...


class RequestSetupError(RequestError):
    ...


class IdentifierError(RequestSetupError):
    ...


class ResponseHandlingError(Error):
    ...


class ResponseError(Error):
    def __init__(self, resp: dict[str, Any]) -> None:
        ...

    @staticmethod
    def factory(resp: dict[str, Any]) -> Exception:
        ...


class UnauthorizedError(ResponseError):
    ...


class NotFoundError(ResponseError):
    ...


class UnprocessableEntityError(ResponseError):
    ...


class DataConsistencyError(Error):
    ...


class EmbedNotFound(Error):
    def __init__(self, embed_name: str) -> None:
        ...


class RemovedIn27Warning(DeprecationWarning):
    ...


class RemovedIn28Warning(PendingDeprecationWarning):
    ...


class APIDeprecationWarning(DeprecationWarning):
    ...
