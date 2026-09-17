"""
Unit tests for string formatters
"""
from uuid import uuid4
from datetime import datetime
from conductor.src.helpers.format_helpers import timestamp_format, log_format


def test_timestamp_format_should_convert_datetime_to_rfc_5322_timestamp():
    """ timestamp format should format datetime to RFC 5322 GMT timestamp """
    timestamp = datetime(2020, 2, 1, 22, 15, 13)
    expected_timestamp = "Sat, 1 Feb 2020 22:15:13 GMT"
    assert timestamp_format(timestamp) == expected_timestamp


def test_log_format_should_format_args_in_logfmt():
    """ log_format should return string in logfmt format """
    request_id = str(uuid4())
    message = "Request made"
    params = {"data": "foo"}
    expected_message = f'request_id="{request_id}" message="{message}" data="{params["data"]}"'
    formatted_message = log_format(request_id, message, params)
    assert expected_message == formatted_message
