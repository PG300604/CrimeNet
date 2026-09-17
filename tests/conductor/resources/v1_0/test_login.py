"""
Test login resource
"""
from falcon.testing import TestClient
from conductor.src.helpers.auth_helpers import read_token
from conductor.src.helpers.validate_schema import InputMachingError


def test_login_should_return_access_token_on_post(client: TestClient, headers):
    """ login resource should return dictionary with 'accessToken' property, that contains valid token """
    payload = {
        "username": "admin",
        "password": "Pass1234"
    }
    response = client.simulate_post("/v1.0/login", json=payload, headers=headers)
    decoded_claims = read_token(response.json["accessToken"], ["username"])
    assert decoded_claims["username"] == payload["username"]
