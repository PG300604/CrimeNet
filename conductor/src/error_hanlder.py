"""
Handle API errors
"""
from traceback import format_tb
from falcon import (
    HTTPError,
    Request,
    Response)
from .. import api
from .exceptions import APIError, ErrorDetail
from .helpers.log_helpers import log_error, log_exception


def hanlde_errors(request: Request, response: Response, exception: HTTPError, params):
    """ Create API error responses """
    if issubclass(exception.__class__, HTTPError):
        exception = APIError.from_http_error(exception)
    response.status = exception.response_code
    response.media = exception.to_dict(request.context.request_id)
    log_error(request.context.request_id, exception)


def handle_any_error(req: Request, resp: Response, exception: Exception, params):
    """ Handle server errors """
    traceback = "".join(format_tb(exception.__traceback__))
    traceback_detail = ErrorDetail("ExceptionTraceback", "code", traceback)
    error = APIError(str(exception), "api", [traceback_detail])
    resp.status = error.response_code
    resp.media = error.to_dict(req.context.request_id)
    log_exception(req.context.request_id, error.message, traceback)


api.add_error_handler(Exception, handle_any_error)
api.add_error_handler([HTTPError, APIError], hanlde_errors)
