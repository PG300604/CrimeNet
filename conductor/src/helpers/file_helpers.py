"""
Helpers to deal with files
"""
from os.path import isfile
from falcon import HTTP_400
from ..exceptions import ValidationError


CHUNK_SIZE = 4096


class FileExistsError(ValidationError):
    """ Error saving file, file already exists """
    code = "FileExistsError"
    response_code = HTTP_400


def save_file(file, path):
    """
    Saves file into given path

    :param file: WTForms file
    :param path: Path for the file
    :raises FileExistsError: Can't create file, because file with given name already exists
    :returns: path to the file
    """
    if isfile(path):
        raise FileExistsError("File already exists!", "filename")
    with open(path, "wb") as writefile:
        while True:
            buffer = file.read(CHUNK_SIZE)
            if not buffer:
                break
            writefile.write(buffer)
    return path


def stream_file(filepath):
    """
    Stream file by path

    :param filepath: path to the file to be streamed
    """
    with open(filepath, "rb") as read_file:
        while True:
            buffer = read_file.read(CHUNK_SIZE)
            if not buffer:
                break
            yield buffer
