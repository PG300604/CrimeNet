"""
Unit tests for task resource
"""
from os.path import isfile
from unittest.mock import patch, MagicMock, ANY
from requests_toolbelt import MultipartEncoder
from falcon.testing import TestClient
from conductor.src.auth_models import User
from storage.builtin_datasets import BuiltinDataset


def test_task_should_return_ValidationError_if_no_form_or_data_or_dataset_found_in_body_of_post_request(client: TestClient, prepared_header):
    """ post request on task resource should return ValidationError if body doesn't contain form or data or dataset json """
    result = client.simulate_post("/v1.0/tasks/pepe", headers=prepared_header, json={})
    assert result.status_code == 400


def test_task_should_create_perform_analysis_file_task_and_return_operation_id_in_operation_location_on_post(client: TestClient, prepared_header, prepared_file, prepared_user: User):
    """ post request on task resource with form should create perform_analysis_file task with filepath to saved file """
    filename = "testfile.json"
    multipart_data = {
        "options": '{"method": "authority", "parameters": {}}',
        "file": (filename, prepared_file, "application/json")
    }
    multipart_file = MultipartEncoder(
        fields=multipart_data
    )
    prepared_header["Content-Type"] = multipart_file.content_type
    result_mock = MagicMock()
    result_mock.id = "super-id"
    with patch("conductor.src.resources.tasks.perform_analysis_file") as task_mock:
        task_mock.delay.return_value = result_mock
        response = client.simulate_post("/v1.0/tasks/pepe", headers=prepared_header, body=multipart_file.to_string())
        task_mock.delay.assert_called_once_with(
            str(prepared_user.get_folder_path() / filename),
            "pepe",
            {"method": "authority", "parameters": {}},
            ANY,  # datetime
            None)
        assert isfile(prepared_user.get_folder_path() / filename)
        assert response.status_code == 202
        assert result_mock.id in response.headers["Operation-Location"]


def test_task_should_return_FormValidationError_if_form_key_not_found(client: TestClient, prepared_header):
    """ post request on task resource without file filed should return 400 response """
    filename = "testfile.json"
    multipart_data = {
        "options": '{"method": "authority", "parameters": {}}',
    }
    multipart_file = MultipartEncoder(
        fields=multipart_data
    )
    prepared_header["Content-Type"] = multipart_file.content_type
    with patch("conductor.src.resources.tasks.perform_analysis_file") as task_mock:
        response = client.simulate_post("/v1.0/tasks/pepe", headers=prepared_header, body=multipart_file.to_string())
        task_mock.delay.assert_not_called()
        assert response.status_code == 400


def test_task_should_return_ValidationError_if_options_or_parameters_are_not_json_strings(client: TestClient, prepared_header, prepared_file):
    """ post request on task resource with invalid json in options or parameters fields should return 400 response """
    filename = "testfile.json"
    multipart_data = {
        "options": '{"method": "parameters": {}}',
        "file": (filename, prepared_file, "application/json")
    }
    multipart_file = MultipartEncoder(
        fields=multipart_data
    )
    prepared_header["Content-Type"] = multipart_file.content_type
    with patch("conductor.src.resources.tasks.perform_analysis_file") as task_mock:
        response = client.simulate_post("/v1.0/tasks/pepe", headers=prepared_header, body=multipart_file.to_string())
        task_mock.delay.assert_not_called()
        assert response.status_code == 400


def test_task_should_create_perform_analysis_network_when_network_in_request_body_on_post_request(client: TestClient, prepared_header, prepared_user: User):
    """ post request on task resource with network field should create perform_analysis_network task  """
    data = {
        "network": [
            {"type": "node", "id": "Satam_Suqami", "properties": {"type": "person", "name": "Satam Suqami", "flight": "AA #11 WTC North", "attend_Las_Vegas_Meeting": False}},
            {"type": "edge", "source": "Majed_Moqed", "target": "Khalid_Al-Mihdhar", "properties": {"type": "prior_contact", "observed": True, "weight": 1}}
        ],
        "options": {
            "method": "authority",
            "parameters": {}
        }
    }
    compare_dataset = BuiltinDataset(None, from_file=False)
    compare_dataset.save_nodes({"Satam_Suqami": {"type": "person", "name": "Satam Suqami", "flight": "AA #11 WTC North", "attend_Las_Vegas_Meeting": False}})
    compare_dataset.save_edges([{"source": "Majed_Moqed", "target": "Khalid_Al-Mihdhar", "properties": {"type": "prior_contact", "observed": True, "weight": 1}}])
    result_mock = MagicMock()
    result_mock.id = "super-id"
    with patch("conductor.src.resources.tasks.perform_analysis_network") as task_mock:
        task_mock.delay.return_value = result_mock
        result = client.simulate_post("/v1.0/tasks/pepe", headers=prepared_header, json=data)
        task_mock.delay.assert_called_once_with(
            {
                "task_id": "pepe",
                "network": compare_dataset.get_network(),
                "options": data["options"]
            },
            ANY,
            None
        )
        assert result.status_code == 202
        assert result_mock.id in result.headers["Operation-Location"]


def test_task_should_create_perform_analysis_network_when_dataset_in_request_body_on_post_request(client: TestClient, prepared_header, prepared_user: User):
    """ post request on task resource with dataset field should create perform_analysis_network task """
    data = {
        "dataset": "test",
        "options": {
            "method": "authority",
            "parameters": {}
        }
    }
    prepared_user.create_dataset(data["dataset"], "", None)
    compare_dataset = prepared_user.get_dataset(data["dataset"])
    compare_dataset.save_nodes({"Satam_Suqami": {"type": "person", "name": "Satam Suqami", "flight": "AA #11 WTC North", "attend_Las_Vegas_Meeting": False}})
    compare_dataset.save_edges([{"source": "Majed_Moqed", "target": "Khalid_Al-Mihdhar", "properties": {"type": "prior_contact", "observed": True, "weight": 1}}])
    result_mock = MagicMock()
    result_mock.id = "super-id"
    with patch("conductor.src.resources.tasks.perform_analysis_network") as task_mock:
        task_mock.delay.return_value = result_mock
        result = client.simulate_post("/v1.0/tasks/pepe", headers=prepared_header, json=data)
        task_mock.delay.assert_called_once_with(
            {
                "task_id": "pepe",
                "network": compare_dataset.get_network(),
                "options": data["options"]
            },
            ANY,
            None
        )
        assert result.status_code == 202
        assert result_mock.id in result.headers["Operation-Location"]
