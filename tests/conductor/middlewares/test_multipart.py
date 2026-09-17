"""
FormComponent tests
"""
import pytest
from io import BytesIO
from unittest.mock import MagicMock, patch
from ....conductor.src.middlewares.multipart import FormComponent


@pytest.fixture
def prepared_request():
    """ Set multipart request """
    request = MagicMock()
    request.stream = BytesIO(b"form")
    request.content_type = "multipart/form-data"
    request.env = MagicMock()
    return request

def test_form_component_should_process_request_stream_as_FieldStorage(prepared_request):
    """ FormComponent should take Request.stream and read it with cgi.FieldStorage if content-type is 'multipart/form-data'"""
    with patch("cgi.FieldStorage") as field_mock:
        form_storage = MagicMock()
        field_mock.return_value = form_storage
        middleware = FormComponent()
        middleware.process_request(prepared_request, MagicMock())
        assert prepared_request.context.form == form_storage


def test_form_component_should_set_request_context_form_with_FieldStorage(prepared_request):
    """ FormComponent should take Request.stream and read it with cgi.FieldStorage and put it in Request.context.form if content-type is 'multipart/form-data'"""
    with patch("cgi.FieldStorage") as field_mock:
        middleware = FormComponent()
        middleware.process_request(prepared_request, MagicMock())
        field_mock.assert_called_once_with(fp=prepared_request.stream, environ=prepared_request.env, keep_blank_values=1)
