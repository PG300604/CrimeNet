"""
Unit tests for file resource
"""
import pytest
from os.path import isfile
from unittest.mock import patch
from falcon.testing import TestClient
from requests_toolbelt import MultipartEncoder
from conductor.src.auth_models import User, Role
from .conftest import EXAMPLE_NETWORK


def test_file_should_return_file_contents_on_get(client: TestClient, prepared_header, prepared_user: User):
    """ get request on file resource should return file contents """
    filename = "file1.json"
    file_contents = "example text"
    with open(prepared_user.get_folder_path() / filename, "w+") as file:
        file.write(file_contents)
    response = client.simulate_get("/v1.0/files/" + filename, headers=prepared_header)
    assert response.text == file_contents


def test_file_resource_should_upload_file_by_filename_on_post(client: TestClient, prepared_header, prepared_file, prepared_user: User):
    """ post request on file resource should upload new file """
    filename = "testfile.json"
    multipart_file = MultipartEncoder(
        fields={
            "file": (filename, prepared_file, "application/json")
        }
    )
    prepared_header["Content-Type"] = multipart_file.content_type
    response = client.simulate_post("/v1.0/files/" + filename, body=multipart_file.to_string(), headers=prepared_header)
    with open(prepared_user.get_folder_path() / filename, "r+") as saved_file:
        assert "".join(saved_file.readlines()) == EXAMPLE_NETWORK
        assert response.headers["Location"] == "/v1.0/files/" + filename
        assert response.status_code == 201


def test_file_resource_should_remove_file_on_delete_request(client: TestClient, prepared_header, prepared_user: User):
    """ delete request on file resource should remove the file from user folder """
    filename = "testfile.json"
    with open(prepared_user.get_folder_path() / filename, "w+") as saved_file:
        saved_file.write(r"""{"id": "some other data!"}""")
    response = client.simulate_delete("/v1.0/files/" + filename, headers=prepared_header)
    print(response.text)
    assert response.status_code == 200
    assert not isfile(prepared_user.get_folder_path() / filename)


def test_file_resource_should_upload_file_by_filename_if_file_does_not_exist_on_put(client: TestClient, prepared_header, prepared_file, prepared_user: User):
    """ put request on file resource should add new file if it doesn't exists """
    filename = "testfile.json"
    multipart_file = MultipartEncoder(
        fields={
            "file": (filename, prepared_file, "application/json")
        }
    )
    prepared_header["Content-Type"] = multipart_file.content_type
    with open(prepared_user.get_folder_path() / filename, "w+") as saved_file:
        saved_file.write(r"""{"id": "some other data!"}""")
    response = client.simulate_put("/v1.0/files/" + filename, body=multipart_file.to_string(), headers=prepared_header)
    with open(prepared_user.get_folder_path() / filename, "r+") as saved_file:
        assert "".join(saved_file.readlines()) == EXAMPLE_NETWORK
        assert response.status_code == 200


def test_file_resource_should_replace_file_by_filename_if_file_exists_on_put(client: TestClient, prepared_header, prepared_file, prepared_user: User):
    """  """
    """ put request on file resource should add new file if it doesn't exists """
    filename = "testfile.json"
    multipart_file = MultipartEncoder(
        fields={
            "file": (filename, prepared_file, "application/json")
        }
    )
    prepared_header["Content-Type"] = multipart_file.content_type
    response = client.simulate_put("/v1.0/files/" + filename, body=multipart_file.to_string(), headers=prepared_header)
    with open(prepared_user.get_folder_path() / filename, "r+") as saved_file:
        assert "".join(saved_file.readlines()) == EXAMPLE_NETWORK
        assert response.headers["Location"] == "/v1.0/files/" + filename
        assert response.status_code == 201
