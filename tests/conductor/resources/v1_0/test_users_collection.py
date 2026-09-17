"""
Tests for user collection resource
"""
from unittest.mock import patch
import pytest
from falcon import HTTP_201
from falcon.testing import TestClient
from conductor.src.hooks.secure_resource import NotAuthorizedError, NotEnoughPrivileges
from conductor.src.helpers.auth_helpers import create_token
from conductor.src.auth_models import User, Role
from storage.builtin_datasets import BuiltinDataset


@pytest.fixture
def prepared_auth_dataset():
    """ patch dataset for authentication """
    with patch("conductor.src.resources.users_collection.auth_dataset", BuiltinDataset("", from_file=False)) as mock_dataset:
        Role(mock_dataset).add_role("User", 0)
        Role(mock_dataset).add_role("Admin", 1)
        l3s_user = User(mock_dataset).store_user("l3s", "Superpassword1111", "User")
        admin_user = User(mock_dataset).store_user("admin", "Pass1234", "Admin")
        yield mock_dataset
        l3s_user.delete()
        admin_user.delete()


def test_users_collection_get_should_return_list_of_all_users(client: TestClient, auth_headers, prepared_auth_dataset):
    """ get request on users collection resource should list all users """
    response = client.simulate_get("/v1.0/users", headers=auth_headers)
    decoded_payload = response.json
    expected_payload = [
        {"username": u.get_username(), "role": u.role.get_name()}
        for u in User.get_all(prepared_auth_dataset)
    ]
    assert all([ex == de for ex, de in zip(expected_payload, decoded_payload["users"])])


def test_users_collection_post_should_add_new_user_in_auth_graph(client: TestClient, auth_headers, prepared_auth_dataset):
    """ post request on users collection resource should add new user """
    payload = {
        "username": "billy",
        "password": "Superpass9999",
        "role": "User"
    }
    response = client.simulate_post("/v1.0/users", json=payload, headers=auth_headers)
    assert User(prepared_auth_dataset).authenticate(payload["username"], payload["password"])


def test_users_collection_post_should_return_201_response_with_Location_header(client: TestClient, auth_headers, prepared_auth_dataset):
    """ post request on users resource collection should add Location header with link to user and return 201 response """
    payload = {
        "username": "billy",
        "password": "Superpass9999",
        "role": "User"
    }
    response = client.simulate_post("/v1.0/users", json=payload, headers=auth_headers)
    assert response.status == HTTP_201
    assert response.headers["Location"] == "/v1.0/users/" + payload["username"]
