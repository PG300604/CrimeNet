"""
Test opeartions resource
"""
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from falcon.testing import TestClient
from conductor.src.auth_models import User


def test_operations_resource_should_get_task_data_if_it_is_successful(client: TestClient, prepared_header, prepared_user: User):
    """ get request on operations resource should return operation result if it is completed successfully """
    task_response = {
        "createdDateTime": str(datetime.now()),
        "lastActionDateTime": str(datetime.now()),
        "status": "SUCCESS",
        "description": "Analysis resulted successfully",
        "result": {}
    }
    with patch("conductor.src.resources.operations.celery") as celery_mock:
        result_mock = MagicMock()
        result_mock.ready.return_value = True
        result_mock.get.return_value = task_response
        celery_mock.AsyncResult.return_value = result_mock
        result = client.simulate_get("/v1.0/operations/pepe", headers=prepared_header)
        assert result.json["taskData"] == task_response
        assert result.status_code == 200


def test_operations_resource_should_return_info_if_task_is_not_ready(client: TestClient, prepared_header, prepared_user: User):
    """ get request on operations resource should return info if task.ready is false """
    task_response = {
        "createdDateTime": str(datetime.now()),
        "lastActionDateTime": str(datetime.now()),
        "status": "RUNNING",
        "description": "Running task",
        "result": {}
    }
    with patch("conductor.src.resources.operations.celery") as celery_mock:
        result_mock = MagicMock()
        result_mock.ready.return_value = False
        result_mock.info = task_response
        celery_mock.AsyncResult.return_value = result_mock
        result = client.simulate_get("/v1.0/operations/pepe", headers=prepared_header)
        assert result.json["taskData"] == task_response
        assert result.status_code == 200


def test_operations_should_forget_task_if_delete_request_issued(client: TestClient, prepared_header, prepared_user: User):
    """ delete request on operations resource should call forget() method on task """
    with patch("conductor.src.resources.operations.celery") as celery_mock:
        result_mock = MagicMock()
        celery_mock.AsyncResult.return_value = result_mock
        result = client.simulate_delete("/v1.0/operations/pepe", headers=prepared_header)
        result_mock.forget.assert_called_once()
        assert result.status_code == 200
