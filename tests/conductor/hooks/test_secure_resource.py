"""
Tests for Secure hook
"""
from unittest.mock import MagicMock
import pytest
from ....conductor.src.hooks.secure_resource import Secure, NotEnoughPrivileges, NotAuthorizedError
from ....storage.builtin_datasets import BuiltinDataset
from ....conductor.src.auth_models import User, Role


@pytest.fixture
def prepared_data():
    """ Prepare user and roles for authentification """
    dataset = BuiltinDataset("", from_file=False)
    role = Role(dataset).add_role("User", 0)
    bigger_role = Role(dataset).add_role("Admin", 1)
    user = User(dataset).store_user("admin", "Pass1234", "User")
    return (dataset, role, user)


@pytest.fixture
def request_mock(prepared_data):
    """ Prepare mock for Request """
    mock = MagicMock()
    mock.context.user = prepared_data[2]
    return mock


def test_secure_should_raise_NotAuthorizedError_if_no_user_in_request_context(request_mock):
    """ Secure should raise NotAuthorizedError when no user found """
    secure_hook = Secure()
    request_mock.context.user = None
    with pytest.raises(NotAuthorizedError):
        secure_hook(request_mock, MagicMock(), MagicMock(), MagicMock())

def test_secure_should_raise_NotEnoughPrivileges_if_role_with_higher_rank_required(request_mock):
    """ Secure should raise NotEnoughPrivileges when user role has smaller rank, than the one that needed """
    secure_hook = Secure("Admin")
    with pytest.raises(NotEnoughPrivileges):
        secure_hook(request_mock, MagicMock(), MagicMock(), MagicMock())
