"""
Helpers for logging
"""
import logging
from .format_helpers import log_format
from ..exceptions import APIError


def log_event(request_id: str, message: str, **kwargs):
    """ Log an INFO message """
    logger = logging.getLogger("api")
    logger.info(log_format(request_id, message, kwargs))


def log_error(request_id, error: APIError):
    """ Log normal error handling """
    logger = logging.getLogger("api")
    params = {
        "code": error.code,
        "response_code": error.response_code,
        "target": error.target
    }
    logger.error(
        log_format(
            request_id,
            error.message,
            params))


def log_exception(request_id: str, message: str, traceback: str):
    """ Log unhandled exception """
    logger = logging.getLogger("api")
    logger.critical(
        log_format(
            request_id,
            message,
            {"traceback": traceback}))
