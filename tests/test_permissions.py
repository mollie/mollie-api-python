import pytest

from mollie.api.error import IdentifierError
from mollie.api.objects.permission import Permission
from mollie.api.resources.permissions import Permissions

from .utils import assert_list_object

PERMISSION_ID = "payments.read"


def test_list_permissions(oauth_client, response):
    """Retrieve a list of existing permissions."""
    response.get("https://api.mollie.com/v2/permissions", "permissions_list")

    permissions = oauth_client.permissions.list()
    assert_list_object(permissions, Permission)


def test_get_permission(oauth_client, response):
    """Retrieve a single permission."""
    response.get(f"https://api.mollie.com/v2/permissions/{PERMISSION_ID}", "permission_single")

    permission = oauth_client.permissions.get(PERMISSION_ID)
    assert isinstance(permission, Permission)
    assert permission.id == PERMISSION_ID
    assert permission.resource == "permission"
    assert permission.description == "View your payments"
    assert permission.granted is True


@pytest.mark.parametrize(
    "input,expected",
    [
        (None, IdentifierError),
        ("foo", IdentifierError),
        ("foo.", IdentifierError),
        (".bar", IdentifierError),
        ("foo1", IdentifierError),
        ("foo1.", IdentifierError),
        (".bar1", IdentifierError),
        ("foo.bar1", IdentifierError),
        ("foo1.bar", IdentifierError),
        ("foo.bar", None),  # Valid
    ],
)
def test_validate_permission_id(input, expected):
    if expected == IdentifierError:
        with pytest.raises(IdentifierError):
            Permissions.validate_permission_id(input)
    else:
        assert Permissions.validate_permission_id(input) is expected
