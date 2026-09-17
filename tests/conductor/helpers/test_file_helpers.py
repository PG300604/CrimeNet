"""
Test file helpers
"""
import pytest
from unittest.mock import MagicMock, patch
from ....conductor.src.helpers.file_helpers import save_file, FileExistsError, CHUNK_SIZE


def test_save_file_should_copy_file_into_file_on_disc():
    """ save_file should read passed file and write it into new file if file does not exists """
    file_mock = MagicMock()
    file_mock.read.return_value = None
    filepath = "/tmp/files/file.json"
    with patch("sna.conductor.src.helpers.file_helpers.isfile") as file_checker:
        file_checker.return_value = False
        with patch("sna.conductor.src.helpers.file_helpers.open") as open_mock:
                save_file(file_mock, filepath)
                file_mock.read.assert_called_once_with(CHUNK_SIZE)


def test_save_file_should_raise_FileExistsError_if_file_on_given_path_exists():
    """ save_file should raise FileExistsError if isfile returns True """
    file_mock = MagicMock()
    filepath = "/tmp/files/file.json"
    with patch("sna.conductor.src.helpers.file_helpers.isfile") as file_checker:
        file_checker.return_value = True
        with pytest.raises(FileExistsError):
            save_file(file_mock, filepath)
