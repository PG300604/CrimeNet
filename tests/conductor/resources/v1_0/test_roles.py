"""
Unit tests for role resource
"""
import pytest
from unittest.mock import patch
from falcon.testing import TestClient
from requests_toolbelt import MultipartEncoder
from storage.builtin_datasets import BuiltinDataset
from conductor.src.auth_models import User, Role, AuthRecordNotFoundError


@pytest.fixture
def prepared_auth_dataset():
    """ patch dataset for authentication """
    with patch("conductor.src.resources.roles.auth_dataset", BuiltinDataset("", from_file=False)) as mock_dataset:
        Role(mock_dataset).add_role("User", 0)
        Role(mock_dataset).add_role("Admin", 1)
        admin_user = User(mock_dataset).store_user("admin", "Pass1234", "Admin")
        yield mock_dataset
        admin_user.delete()


def test_role_resource_should_return_role_rank_on_get_request(client: TestClient, auth_headers, prepared_auth_dataset):
    """ get request on role resource should return name and rank of the role """
    role_name = "Admin"
    response = client.simulate_get("/v1.0/roles/" + role_name, headers=auth_headers)
    payload = response.json
    expected_role = Role(prepared_auth_dataset).get_role_vertex(role_name)
    assert payload["name"] == expected_role.get_name()
    assert payload["rank"] == expected_role.get_rank()


def test_role_resource_should_create_new_role_on_post_request(client: TestClient, auth_headers, prepared_auth_dataset):
    """ post request on role resource should create new role """
    role_name = "Onlooker"
    payload = {
        "rank": 2
    }
    response = client.simulate_post("/v1.0/roles/" + role_name, headers=auth_headers, json=payload)
    created_role = Role(prepared_auth_dataset).get_role_vertex(role_name)
    assert response.status_code == 201
    assert payload["rank"] == created_role.get_rank()


def test_role_resource_should_return_AlreadyExistsError_if_role_exists_on_post_request(client: TestClient, auth_headers, prepared_auth_dataset):
    """ post request on role resource should return AlreadyExistsError with 400 response code if role already exists """
    role_name = "Admin"
    payload = {
        "rank": 1
    }
    response = client.simulate_post("/v1.0/roles/" + role_name, headers=auth_headers, json=payload)
    assert response.status_code == 400


def test_role_resource_should_update_role_parameters_on_patch_request(client: TestClient, auth_headers, prepared_auth_dataset):
    """ patch request should update role name or rank on patch request """
    role_name = "Admin"
    payload = {
        "rank": 2
    }
    response = client.simulate_patch("/v1.0/roles/" + role_name, headers=auth_headers, json=payload)
    created_role = Role(prepared_auth_dataset).get_role_vertex(role_name)
    assert created_role.get_rank() == payload["rank"]
    assert response.status_code == 200


def test_role_resource_should_create_role_if_role_does_not_exist_on_patch_request(client: TestClient, auth_headers, prepared_auth_dataset):
    """ patch request should create new role if role not found """
    role_name = "Onlooker"
    payload = {
        "rank": 2
    }
    response = client.simulate_patch("/v1.0/roles/" + role_name, headers=auth_headers, json=payload)
    created_role = Role(prepared_auth_dataset).get_role_vertex(role_name)
    assert created_role.get_rank() == payload["rank"]
    assert response.status_code == 201
