"""
Unit tests for algorithms collection
"""
import pytest
from unittest.mock import patch
from falcon import HTTP_201
from falcon.testing import TestClient
from conductor.src.auth_models import User


def test_algorithms_resource_should_return_algorithm_info_on_get_request(client: TestClient, prepared_header, prepared_user: User):
    """ get request on algorithms resource should return edited analyzer info """
    example_info = {
        "community_detection": {
            "methods": {
                "asyn_lpa": {
                    "name": "Asynchronous Label Propagation",
                    "parameter": {}
                }
            }
        },
        "node_embedding": {
            "methods": {
                "nmf": {
                    "name": "Non-negative Matrix Factorization",
                    "parameter": {
                        "K": {
                            "description": "The embedding dimension",
                            "options": {
                                "Integer": "Integer"
                            }
                        }
                    }
                }
            }
        }
    }
    expected_info = {
        "tasks": [
            {
                "name": "community_detection",
                "methods": [
                    {
                        "name": "asyn_lpa",
                        "description": "Asynchronous Label Propagation",
                        "parameter": {}
                    }
                ]
            },
            {
                "name": "node_embedding",
                "methods": [
                    {
                        "name": "nmf",
                        "description": "Non-negative Matrix Factorization",
                        "parameter": {
                            "K": {
                                "description": "The embedding dimension",
                                "options": {
                                    "Integer": "Integer"
                                }
                            }
                        }
                    }
                ]
            }
        ]
    }
    with patch("conductor.src.resources.tasks_collection.request_taker") as analyzer_mock:
        analyzer_mock.get_info.return_value = example_info
        result = client.simulate_get("/v1.0/tasks", headers=prepared_header)
        assert result.json == expected_info
