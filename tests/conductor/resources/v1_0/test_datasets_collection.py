"""
Tests for datasets collection resource
"""
import pytest
import tempfile
import shutil
from os.path import isfile
from unittest.mock import patch
from falcon.testing import TestClient
from requests_toolbelt import MultipartEncoder
from conductor.src.auth_models import User, DatasetDoesNotExistError
from .conftest import EXAMPLE_NETWORK
from storage.builtin_datasets import BuiltinDataset

def test_datasets_should_list_users_datasets_on_get_request(client: TestClient, prepared_header, prepared_user: User):
    """ get on datasets collection should list all datasets of the user """
    dataset_names = ["first", "second"]
    prepared_user.create_dataset(dataset_names[0], "Test dataset 1", None)
    prepared_user.create_dataset(dataset_names[1], "Test dataset 2", None)
    response = client.simulate_get("/v1.0/datasets", headers=prepared_header)
    assert all([dataset in response.json["datasets"] for dataset in dataset_names])


def test_datasets_should_create_new_dataset_on_post_request(client: TestClient, prepared_header, prepared_user: User):
    """ post on datasets collection should create new dataset with given name and description """
    dataset_info = {
        "datasetName": "first",
        "datasetDescription": "Description"
    }
    response = client.simulate_post("/v1.0/datasets", headers=prepared_header, json=dataset_info)
    assert response.status_code == 201
    assert prepared_user.get_dataset(dataset_info["datasetName"])


def test_datasets_should_create_new_dataset_from_file_on_post_request_if_datasetFile_property_provided(client: TestClient, prepared_header, prepared_user: User):
    """ post on datasets collection with uploadFile filename should create new dataset from file """
    filename = "datafile.json"
    with open(prepared_user.get_folder_path() / filename, "w+") as file:
        file.write(EXAMPLE_NETWORK)
    dataset_info = {
        "datasetName": "first",
        "datasetDescription": "Description",
        "uploadFile": filename
    }
    response = client.simulate_post("/v1.0/datasets", headers=prepared_header, json=dataset_info)
    created_dataset = prepared_user.get_dataset(dataset_info["datasetName"])
    dataset_compare = BuiltinDataset(str(prepared_user.get_folder_path() / filename))
    assert all([created_dataset.nodes[k] == dataset_compare.nodes[k] for k in dataset_compare.nodes])
    assert all([created_dataset.adj_list[k] == dataset_compare.adj_list[k] for k in dataset_compare.adj_list])
    assert created_dataset.edges == dataset_compare.edges
    assert created_dataset.node_types == dataset_compare.node_types
    assert created_dataset.edge_types == dataset_compare.edge_types
    assert response.status_code == 201


def test_datasets_should_create_new_dataset_from_uploaded_file_if_request_is_multipart(client: TestClient, prepared_header, prepared_user: User):
    """ post on datasets collection with multipart request type should create dataset from file in file with name 'datasetName' """
    filename = "testfile.json"
    dataset_name = "first"
    tempdir = tempfile.mkdtemp()
    file = open(tempdir + filename, "wb+")
    file.write(EXAMPLE_NETWORK.encode())
    file.seek(0)
    multipart_file = MultipartEncoder(
        fields={
            "datasetName": dataset_name,
            "datasetDescription": "This is good stuff",
            "file": (filename, file, "application/json")
        }
    )
    prepared_header["Content-Type"] = multipart_file.content_type
    response = client.simulate_post("/v1.0/datasets", headers=prepared_header, body=multipart_file.to_string())
    file.close()
    created_dataset = prepared_user.get_dataset(dataset_name)
    dataset_compare = BuiltinDataset(tempdir + filename)
    assert all([created_dataset.nodes[k] == dataset_compare.nodes[k] for k in dataset_compare.nodes])
    assert all([created_dataset.adj_list[k] == dataset_compare.adj_list[k] for k in dataset_compare.adj_list])
    assert created_dataset.edges == dataset_compare.edges
    assert created_dataset.node_types == dataset_compare.node_types
    assert created_dataset.edge_types == dataset_compare.edge_types
    assert response.status_code == 201
    shutil.rmtree(tempdir)


def test_datasets_should_dump_dataset_into_user_folder_if_dumpFile_provided(client: TestClient, prepared_header, prepared_user: User):
    """ post on datasets collection with dumpFile property should dump dataset into user folder """
    filename = "datafile.json"
    dataset_info = {
        "datasetName": "first",
        "dumpFile": filename
    }
    prepared_user.create_dataset(dataset_info["datasetName"], "stuff", None)
    response = client.simulate_post("/v1.0/datasets", headers=prepared_header, json=dataset_info)
    isfile(prepared_user.get_folder_path() / filename)
    assert response.status_code == 201


def test_datasets_should_remove_dataset_on_delete_request(client: TestClient, prepared_header, prepared_user: User):
    """ delete on datasets collection should remove dataset by name from user datasets """
    dataset_info = {
        "datasetName": "dataset"
    }
    prepared_user.create_dataset(dataset_info["datasetName"], "stuff", None)
    response = client.simulate_delete("/v1.0/datasets", headers=prepared_header, json=dataset_info)
    with pytest.raises(DatasetDoesNotExistError):
        prepared_user.get_dataset(dataset_info["datasetName"])
    assert response.status_code == 200
