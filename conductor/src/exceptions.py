"""
Common application exceptions
"""
from uuid import uuid4
from collections import namedtuple
from falcon import HTTPError, HTTP_400, HTTP_500, HTTP_401, HTTP_404, HTTP_409

ErrorDetail = namedtuple("ErrorDetail", ["code", "target", "message"])


class APIError(RuntimeError):
    """ Common API exception """

    code = "APIError"
    response_code = HTTP_500

    def __init__(self, message, target, details=None):
        self.message = message
        self.target = target
        self.details = details

    @classmethod
    def from_http_error(cls, ex: HTTPError):
        """ Create exception class from falocn HTTPError """
        error = cls(ex.title, "HTTP request")
        error.response_code = ex.status
        return error

    @classmethod
    def to_docs_example(cls, message=None, target=None, details=None):
        """ Create Swagger doc form exception """
        return {
            "request_id": str(uuid4()),
            "code": cls.code,
            "message": message if message else "Message here",
            "target": target if target else "Error target",
            "details": details if details else []
        }

    def to_dict(self, request_id: str):
        """ Return dict to be serialized """
        result = {
            "request_id": request_id,
            "code": self.code,
            "message": self.message,
            "target": self.target
        }
        if self.details:
            result["details"] = [{"code": d.code, "target": d.target, "message": d.message} for d in self.details]
        return result

    def __str__(self):
        return self.message


class VersioningError(APIError):
    """ Error with api verion given """
    code = "VersioningError"
    response_code = HTTP_400


class TaskError(APIError):
    """ Error in task preparation or execution """
    code = "TaskError"
    response_code = HTTP_409


class AuthenticationError(APIError):
    """ Error in login, account creation or access verification """
    code = "AuthenticationError"
    response_code = HTTP_401


class ValidationError(APIError):
    """ Error validating user input """
    code = "ValidationError"
    response_code = HTTP_400


class ResourceError(APIError):
    """ Resource either does not exists or unavalible """
    code = "ResourceError"
    response_code = HTTP_404


class FormValidationError(ValidationError):
    """ Error validating form input """
    code = "FormValidationError"
    response_code = HTTP_400


class FileNotFoundError(APIError):
    """ Error finding file """
    code = "FileNotFoundError"
    response_code = HTTP_404


class DatasetError(APIError):
    """ Error within dataset """
    code = "DatasetError"
    response_code = HTTP_500

    @classmethod
    def from_dataset_message(cls, dataset_message):
        """ Create error from dataset message """
        return cls(dataset_message["message"], "dataset")
