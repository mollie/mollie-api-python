import pytest

from mollie.api.error import IdentifierError
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
