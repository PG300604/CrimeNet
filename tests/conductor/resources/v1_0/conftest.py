"""
Configure global fixtures
"""
import pytest
import logging
from unittest.mock import patch
from tempfile import TemporaryFile
from falcon.testing import TestClient
from conductor import api
from conductor.src.auth_models import Role, User
from storage.builtin_datasets import BuiltinDataset, BuiltinDatasetsManager
from conductor.src.helpers.auth_helpers import create_token

EXAMPLE_NETWORK = r"""{"type": "node", "id": "Satam_Suqami", "properties": {"type": "person", "name": "Satam Suqami", "flight": "AA #11 WTC North", "attend_Las_Vegas_Meeting": false}}
{"type": "node", "id": "Wail_Alshehri", "properties": {"type": "person", "name": "Wail Alshehri", "flight": "AA #11 WTC North", "attend_Las_Vegas_Meeting": false}}
{"type": "node", "id": "Majed_Moqed", "properties": {"type": "person", "name": "Majed Moqed", "flight": "AA #77 Pentagon", "attend_Las_Vegas_Meeting": false}}
{"type": "node", "id": "Waleed_Alshehri", "properties": {"type": "person", "name": "Waleed Alshehri", "flight": "AA #11 WTC North", "attend_Las_Vegas_Meeting": false}}
{"type": "node", "id": "Khalid_Al-Mihdhar", "properties": {"type": "person", "name": "Khalid Al-Mihdhar", "flight": "AA #77 Pentagon", "attend_Las_Vegas_Meeting": false}}
{"type": "node", "id": "Nawaf_Alhazmi", "properties": {"type": "person", "name": "Nawaf Alhazmi", "flight": "AA #77 Pentagon", "attend_Las_Vegas_Meeting": true}}
{"type": "node", "id": "Ahmed_Alghamdi", "properties": {"type": "person", "name": "Ahmed Alghamdi", "flight": "UA #175 WTC South", "attend_Las_Vegas_Meeting": false}}
{"type": "edge", "source": "Majed_Moqed", "target": "Khalid_Al-Mihdhar", "properties": {"type": "prior_contact", "observed": true, "weight": 1}}
{"type": "edge", "source": "Majed_Moqed", "target": "Nawaf_Alhazmi", "properties": {"type": "prior_contact", "observed": true, "weight": 1}}
{"type": "edge", "source": "Khalid_Al-Mihdhar", "target": "Majed_Moqed", "properties": {"type": "prior_contact", "observed": true, "weight": 1}}
{"type": "edge", "source": "Khalid_Al-Mihdhar", "target": "Nawaf_Alhazmi", "properties": {"type": "prior_contact", "observed": true, "weight": 1}}
{"type": "edge", "source": "Hani_Hanjour", "target": "Ahmed_Alghamdi", "properties": {"type": "prior_contact", "observed": true, "weight": 1}}
{"type": "edge", "source": "Nawaf_Alhazmi", "target": "Majed_Moqed", "properties": {"type": "prior_contact", "observed": true, "weight": 1}}
"""


@pytest.fixture
def client():
    """ Initialize API client """
    logging.getLogger("api").setLevel(logging.CRITICAL)
    return TestClient(api)


@pytest.fixture
def headers():
    """ Prepare headers for each request """
    return {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


@pytest.fixture
def auth_headers(headers):
    """ Generate admin access token """
    headers["Authorization"] = "Bearer " + create_token({"username": "admin"})
    return headers


@pytest.fixture
def prepared_user():
    """ Prepare user to store files """
    with patch("conductor.src.middlewares.authorization.auth_dataset", BuiltinDataset("", from_file=False)) as mock_dataset, \
        patch("conductor.src.auth_models.data_manager", BuiltinDatasetsManager(None, None)) as mock_manager:
        Role(mock_dataset).add_role("User", 0)
        user = User(mock_dataset).store_user("l3s", "Superpassword1111", "User")
        yield user
        user.delete()


@pytest.fixture
def prepared_header(headers, prepared_user: User):
    """ Generate access token """
    headers["Authorization"] = "Bearer " + create_token({"username": prepared_user.get_username()})
    return headers


@pytest.fixture
def prepared_file():
    """ Create file to send in form """
    file = TemporaryFile(mode="wb+")
    file_contents = EXAMPLE_NETWORK
    file.write(file_contents.encode())
    file.seek(0)
    yield file
    file.close()
