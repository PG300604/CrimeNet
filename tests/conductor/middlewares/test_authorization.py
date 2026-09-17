"""
Test authorization middleware
"""
import pytest
from unittest import mock
from unittest.mock import patch, MagicMock
from ....conductor.src.middlewares.authorization import AuthorizationComponent
from ....conductor.src.helpers.auth_helpers import create_token
from ....conductor.src.auth_models import Role, User
from ....storage.builtin_datasets import BuiltinDataset


@pytest.fixture
def prepared_request():
    """ Prepare Request for middleware """
    request_mock = MagicMock()
    request_mock.auth = AuthorizationComponent.auth_header_prefix + create_token({"username": "admin"})
    return request_mock


def test_process_request_should_add_user_in_context(prepared_request):
    """ If Authorisation header is empty """
    with patch("sna.conductor.src.auth_graph.auth_dataset", BuiltinDataset("", from_file=False)) as dataset:
        auth_middleware = AuthorizationComponent()
        role = Role(dataset).add_role("User", 0)
        user = User(dataset).store_user("admin", "Pass1234", "User")
        auth_middleware.process_request(prepared_request, MagicMock())
        assert prepared_request.context.user.get_username() == "admin"
