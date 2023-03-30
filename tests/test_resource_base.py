import pytest

from mollie.api.error import BadRequestError, IdentifierError, ResponseHandlingError, UnprocessableEntityError
from mollie.api.resources.base import ResourceBase


class MyTestResource(ResourceBase):
    """Minimal resource for testing."""

    RESOURCE_ID_PREFIX = "test_"


def test_validate_resource_id(client):
    resource = MyTestResource(client)
    with pytest.raises(IdentifierError) as excinfo:
        resource.validate_resource_id("invalid")

    assert str(excinfo.value) == "Invalid Identifier 'invalid', it should start with 'test_'."


def test_validate_resource_id_custom_identifier_name(client):
    resource = MyTestResource(client)
    with pytest.raises(IdentifierError) as excinfo:
        resource.validate_resource_id("invalid", name="MockerMockMock")

    assert str(excinfo.value) == "Invalid MockerMockMock 'invalid', it should start with 'test_'."


def test_validate_resource_id_custom_message(client):
    resource = MyTestResource(client)
    with pytest.raises(IdentifierError) as excinfo:
        resource.validate_resource_id("invalid", message="No no no, only tests allowed here!")

    assert str(excinfo.value) == "No no no, only tests allowed here!"


def test_response_handling_error_sets_message_and_key_correctly():
    try:
        raise ResponseHandlingError("This is a ResponseHandlingError", "test_idempotency_key")
    except ResponseHandlingError as exc:
        assert exc.idempotency_key == "test_idempotency_key"
        assert str(exc) == "This is a ResponseHandlingError"


def test_bad_request_error_set_message_and_key_correctly():
    try:
        raise BadRequestError({"detail": "This is a BadRequestError", "status": 400}, "test_idempotency_key")
    except BadRequestError as exc:
        assert exc.idempotency_key == "test_idempotency_key"
        assert str(exc) == "This is a BadRequestError"


def test_conflict_error_set_message_and_key_correctly():
    try:
        raise BadRequestError({"detail": "This is a ConflictError", "status": 409}, "test_idempotency_key")
    except BadRequestError as exc:
        assert exc.idempotency_key == "test_idempotency_key"
        assert str(exc) == "This is a ConflictError"


def test_create_request_without_idempotency_key_sets_idempotency_key_on_error(client, response):
    """Test that an exception contains an auto-generated imdepotency_key, eventhough no idempotency_key was passed."""

    response.post("https://api.mollie.com/v2/payments", "payment_rejected", status=422)

    try:
        client.payments.create({})
    except UnprocessableEntityError as exc:
        assert exc.idempotency_key is not None


def test_create_request_without_idempotency_key_sets_idempotency_key(client, response, mocker):
    """Test that performing a POST request correctly sets and passes the idempotency_key if it does not exist yet."""

    mocked_api_call = mocker.patch("mollie.api.resources.base.ResourceBase.perform_api_call")

    client.payments.create({})
    assert mocked_api_call.call_args.kwargs["idempotency_key"] is not None
